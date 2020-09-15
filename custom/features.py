# -*- coding: utf-8 -*-
##############################################################################
# Author：QQ173782910  /custom/features.py
##############################################################################

# 注意，策略，止盈，止损，这三个方法提供给有需要自定义使用个人的相关处理，

def Strategy():#策略
    # 止盈，止损请判断无策略信号进行处理
    # 策略有效的返回值有五个：1 为开多,-1为开空,11为平多,-11为平空,0为无信号
    # 1,-1,11,-11,0
    return ''#返回空就是表示不使用自定义策略，其他几个信号为使用个人策略处理。

def Stop_profit_now(stop_pnl,pnl_num,pt):#止盈处理
    # stop_pnl:止盈处理类型,pnl_num:止盈量
    # longnum：多单持仓, longcost：多单均价, longpnl：多单盈利, shortnum：空单持仓, shortcost：空单均价, shortpnl：空单盈利, last：最新价
    # 返回值 11,-11   当需要平多返回11，当需要平空返回-11,其他值不处理
    longnum, longcost, longpnl, shortnum, shortcost, shortpnl, last = pt
    # 可选值说明
    # 0:由策略自动处理；
    # 1:“获利止盈”就是当收益大于下方填写的“止盈量”时在无策略信号下就平仓;
    # 2:“开仓比止盈”就是当“开仓比”大于下方填写的“止盈量”时在无策略信号下就平仓，
    # 多单“开仓比”=(“最新价”-"开仓价")/"开仓价",空单“开仓比”=("开仓价"-“最新价”)/"开仓价"
    # 3：“开仓比回撤止盈”就是记录的“最高价”或“最低价”，当价格回撤时多单是(“最高价”-“开仓价”)/“开仓价”，
    # 空单是(“开仓价”-“最低价”)/“开仓价”，大于下方填写的“止盈量”在无策略信号下就平仓;
    if stop_pnl==0:
        return ''
    elif stop_pnl==1:
        if longnum>0 and longpnl > pnl_num:#平多
            return 11
        elif shortnum>0 and shortpnl>pnl_num:#平空
            return -11
    elif stop_pnl == 2:
        if longnum > 0 and (last-longcost)/longcost > pnl_num:  # 平多
            return 11
        elif shortnum > 0 and (shortcost-last)/shortcost > pnl_num:  # 平空
            return -11
    return ''



def Stop_loss_now(stop_kx,kx_num,pt):#止损处理
    # stop_kx:止损处理类型,kx_num：止损量
    # longnum：多单持仓, longcost：多单均价, longpnl：多单盈利, shortnum：空单持仓, shortcost：空单均价, shortpnl：空单盈利, last：最新价
    # 返回值 11,-11   当需要平多返回11，当需要平空返回-11,其他值不处理
    longnum, longcost, longpnl, shortnum, shortcost, shortpnl, last = pt
    # 可选值说明 0:由策略自动处理；1:“亏损止损”就是当亏损大于下方填写的“止损量”时在无策略信号下就平仓;
    # 2:“开仓比止损”就是当“开仓比”大于下方填写的“止损量”时在无策略信号下就平仓，
    # 多单：“最新价”比“开仓价”小，“开仓比”=("开仓价"-“最新价”)/"开仓价"
    # 空单：“最新价”比“开仓价”大，“开仓比”=(“最新价”-"开仓价")/"开仓价"
    # 3:“现价止损”就是多单： “现价”<"开仓价"X（1-"止损量"）,空单：“现价”>"开仓价"X（1+"止损量"）
    # 4:“开仓价止损”就是多单： “现价” < "开仓价" - "止损量", 空单：“现价” > "开仓价" + "止损量"
    if stop_kx==0:
        return ''
    elif stop_kx==1:
        if longnum > 0 and longpnl < -kx_num:  # 平多
            return 11
        elif shortnum > 0 and shortpnl < -kx_num:  # 平空
            return -11
    elif stop_kx==2:
        if longnum > 0 and (longcost-last) / longcost > kx_num:  # 平多
            return 11
        elif shortnum > 0 and (last-shortcost) / shortcost > kx_num:  # 平空
            return -11
    elif stop_kx==3:
        if longnum > 0 and last < longcost*(1-kx_num):  # 平多
            return 11
        elif shortnum > 0 and last > shortcost*(1+kx_num):  # 平空
            return -11
    elif stop_kx==4:
        if longnum > 0 and last<(longcost-kx_num):  # 平多
            return 11
        elif shortnum > 0 and last>(shortcost+kx_num):  # 平空
            return -11

    return ''







