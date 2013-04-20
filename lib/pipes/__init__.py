# coding=utf-8
"""@pipes
"""

import glob
import os.path

__all__ = [os.path.basename(f)[:-3] for f in glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
           if os.path.basename(f) != "__init__.py"]

mod_list = [__import__(mod, globals(), locals(), [], - 1) for mod in  __all__]

pipes_dics = {}
for mod in mod_list:
    try:
        register = getattr(mod, "register")
    except:
        continue
    register(pipes_dics)

class InvalidManipulationJSONWarning(UserWarning):
    def __init__(self,name,msg):
        self.name = name
        self.msg = msg
    def __str__(self):
        return "while processing pipe[%s]: %s" % (self.name, self.msg)

def execute(manip):
    """
    execute pipeline
    """
    # TODO write doctest
    run_list = []
    for mn in manip:
        name = mn["name"]
        if name not in pipes_dics:
            raise InvalidManipulationJSONWarning(name,"invalid name")
        dic = pipes_dics[name]
        if len(mn["args"]) != len(dic["args"]):
            raise InvalidManipulationJSONWarning(name,"invalid arguments")
        if "kwds" in mn and "kwds" in dic:
            kwds = {}
            for kwd in mn["kwds"]:
                if kwd not in dic["kwds"]
                    continue
                kwds[kew] = mn["kwds"][kwd]
            run_list = dic["func"](run_list,*mn["args"],**kwds)
        else:
            run_list = dic["func"](run_list,*mn["args"])
    return run_list

import json
def execute_from_json_str(manip_json_str):
    manip = json.loads(manip_json_str)
    execute(manip)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

