## -*- coding: utf-8 -*-
import platform,sys

if platform.system() == "Windows":
    from . import JSW as JS_TOOL
elif platform.system()=="Linux":
    from . import JSL as JS_TOOL
else:
    print("请联系维护.")
    sys.exit(1)
