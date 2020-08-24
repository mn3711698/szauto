
import time
import traceback
import gevent
from gevent import monkey
monkey.patch_all()
from basic import JD_TOOL
from trade import Trade_TOOL
from okex.account_api import AccountAPI

bugerror=JD_TOOL.bugerror
save_log=JD_TOOL.save_log

period=300
count=1

aa=time.time()

class RunTrade():

    def __init__(self,params):#持仓及资产相关的初始化放在这
        #params:[api, secret, passp, symbol, 300时间周期, 1张数, usr_id, status, us_id]
        self.api,self.secret,self.passp,self.symbol,self.periods,self.deal_num,\
        self.stop_pnl,self.pnl_num,self.stop_kx,self.kx_num = params
        if 'SWAP' in self.symbol:
            self.robot = Trade_TOOL.SwapTrade(params)
        else:
            self.robot = Trade_TOOL.FutureTrade(params)
        self.params = params


    def check_authority(self):#检查API密钥，需要API有交易权限，不需要有提币权限。
        account = AccountAPI(self.api,self.secret, self.passp, False)
        try:
            result = account.coin_transfer('', '', 1, 1, 5, sub_account='', instrument_id='', to_instrument_id='')
        except:
            print("密钥校验请求处理有误")
            bugerror(traceback, 'check_authority')  #这里收集BUG,以便我可以及时修复处理
            return 3
        if result["code"] == 30006:
            print("密钥校验有误")
            return 1
        elif result["code"] == 30012:
            print("没有权限哦")
            return 2
        else:
            return 0

    def run(self):
        ###################################start 这里在确保API密钥有交易权限后可以注释掉
        ca=self.check_authority()
        if ca!=0:
            save_log('API密钥有误%s'%ca)
            raise("API密钥有误")
        #################################end
        self.robot.realtrade()#每交易一次，更新仓位，仓位变化做存储，以交易对为基准



def fetch(a):

    try:
        RunTrade(a).run()
    except:
        bugerror(traceback,'begin_run_error')#这里收集BUG,以便我可以及时修复处理
        pass


if __name__ == "__main__":
    save_log('clear_log')#有这行会清理之前的日志
    save_log('机器人开始启动')
    # 目前只支持OKEX交易所，后续将支持火币，币安
    # 请确保对应的帐户有足够的资金或及时充值划转资金，
    api_key = ''  # OKEX交易所的api
    secret_key = ''  # OKEX交易所的secret
    passphrase = ''  # OKEX交易所的passphrase
    symbollist = ["EOS-USD-SWAP","EOS-USD-200925"]  # 交易标的
    #symbol = "EOS-USD-SWAP" # 交易标的
    periods = 300  # 这个是策略要用到的时间周期，以那个周期的K线
    deal_num = 1  # 这个是每次交易多少张

    stop_pnl = 1  # 止盈处理类型 可选值说明：0无，1“获利止盈”，2:开仓比止盈
    # 注本来还有一个“获利回撤止盈”和“开仓比回撤止盈”，但需要动态记录最高收益，
    # 因未采用数据库不方便记录，后续将在数据版本中增加“获利回撤止盈”和“开仓比回撤止盈”

    # 可选值说明 0:由策略自动处理；1:“获利止盈”就是当收益大于下方填写的“止盈量”时在无策略信号下就平仓;
    # 2“开仓比止盈”就是当“开仓比”大于下方填写的“止盈量”时在无策略信号下就平仓，
    # 多单“开仓比”=(“最新价”-"开仓价")/"开仓价",空单“开仓比”=("开仓价"-“最新价”)/"开仓价"
    pnl_num = 0.02  # 止盈量

    stop_kx = 0  # 止损处理类型 可选值说明：0无，1“亏损止损”，2:开仓比止损，
    # 可选值说明 0:由策略自动处理；1:“亏损止损”就是当亏损大于下方填写的“止损量”时在无策略信号下就平仓;
    # 2“开仓比止损”就是当“开仓比”大于下方填写的“止损量”时在无策略信号下就平仓，
    # 多单：“最新价”比“开仓价”小，“开仓比”=("开仓价"-“最新价”)/"开仓价"
    # 空单：“最新价”比“开仓价”大，“开仓比”=(“最新价”-"开仓价")/"开仓价"
    kx_num = 0.015  # 止损量
    # 目前只支持永续及交割两种合约，最好是币本位,建议跑ETH,BTC,本人跑EOS收益很少
    # symbol最好是是里边的其中一个: ["ETH-USD-200925", "BTC-USD-200925","BTC-USD-SWAP","ETH-USD-SWAP","EOS-USD-200925", "EOS-USD-SWAP"]

    '''
    parms数据说明[["上边的api","上边填写的secret","上边填写的passp","交易标的","时间周期","每次交易多少张","止盈处理类型","止盈量","止损处理类型","止损量"]]
    '''

    params = [[api_key,secret_key,passphrase,symbol,periods,deal_num,stop_pnl,pnl_num,stop_kx,kx_num] for symbol in symbollist]
    # 同时运行多个交易标的处理，最好是多核心cpu,如果是1核心的云服务器，没办法同时处理的,执行完一个到一个。
    # 建议用centos运行，可以使用supervisor保持机器人运行，当然windows直接python run_robot.py也可以
    #supervisor参考配置如下
    """
    [program:runsr]
    environment =PYTHONPATH=/var/games/szauto/
    directory = /var/games/szauto/
    command = /usr/bin/python3 run_robot.py
    autostart = true
    autorestart=true
    user = root
    redirect_stderr = true
    stdout_logfile = /var/log/runsr.log
    """
    #默认日志如下:linunx:/var/games/szauto/szauto.log windows:d:/webpy/www/szauto/szauto.log
    while True:
        gevent.joinall([gevent.spawn(fetch,x) for x in params])
        time.sleep(7)#每隔7秒运行一次



