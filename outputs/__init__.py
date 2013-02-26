# coding=utf-8
"""@package DataProcessor.output
"""


import glob
import os.path

__all__ = [os.path.basename(f)[:-3] for f in glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
           if os.path.basename(f) != "__init__.py"]



mod_list = [__import__(mod, globals(), locals(), [], - 1) for mod in  __all__]

outputs_dics = {}
for mod in mod_list:
    try:
        register = getattr(mod, "register")
    except:
        print (format("Warning: module %s does not have register function." % mod.__name__))
        continue
    register(outputs_dics)
