## -*- coding: utf-8 -*-
import platform,sys
if platform.system() == "Windows":
    from . import TradeW as Trade_TOOL
elif platform.system()=="Linux":
    from . import TradeL as Trade_TOOL
else:
    print("请联系维护.")
    sys.exit(1)

