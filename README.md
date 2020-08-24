# szauto

## 本项目只是提供代码，不对使用者因使用本代码实际产生的盈亏负责，毕竟赚了钱也没分给我，亏了钱也只能自己扛

# 说明

## API的权限只需要有交易权限就够了，不要开提币权限！

## API的权限只需要有交易权限就够了，不要开提币权限！

## API的权限只需要有交易权限就够了，不要开提币权限！

本项目封装完整的交易处理逻辑，策略处理逻辑。提供自定义使用自己的策略计算交易信号及止盈止损处理。

目前只支持OKEX交易所，后续将支持火币，币安

请确保对应的帐户有足够的资金或及时充值划转资金，

需要准备好OKEX交易所的api_key，api_key，passphrase。

需要确定您的您的交易标的(instrument_id)

支持windows,Linux,建议运行在centos 7下。

相关配置在run_robot.py文件的if __name__ == "__main__":下，请注意看说明

自定义策略，止盈，止损在custom/features.py

如需源码请联系下方QQ,源码不会提供策略部分。

本项目写死了运行路径，windows在d:/webpy/www/szauto,Linux在/var/games/szauto/。

不是上边的路径无法运行。

同时运行多个交易标的处理，最好是多核心cpu,如果是1核心的云服务器，没办法同时处理的,执行完一个到一个。

建议用centos运行，可以使用supervisor保持机器人运行，当然windows直接python run_robot.py也可以

安装相关库
```python
pip install requests
pip install websockets==6.0
pip install gevent
pip install pandas

```
也可以在szauto目前下执行 pip3 install -r requirements.txt 或 pip install -r requirements.txt
supervisor参考配置如下:

```python
[program:runsr]
environment =PYTHONPATH=/var/games/szauto/
directory = /var/games/szauto/
command = /usr/bin/python3 run_robot.py
autostart = true
autorestart=true
user = root
redirect_stderr = true
stdout_logfile = /var/log/runsr.log
```
    
# 更新日志  2020-08-24 (开源协议为MIT)


2020-08-24
初始上传代码


# 联系
QQ173782910
