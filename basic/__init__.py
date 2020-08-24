## -*- coding: utf-8 -*-
import platform,sys

if platform.system() == "Windows":
    from . import JDW as JD_TOOL
elif platform.system()=="Linux":
    from . import JDL as JD_TOOL
else:
    print("请联系维护.")
    sys.exit(1)
