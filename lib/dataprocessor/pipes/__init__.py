# coding=utf-8
"""@pipes
"""
import glob
import os.path

from ..exception import DataProcessorError


class InvalidPipeError(DataProcessorError):
    pass


__all__ = [os.path.basename(f)[:-3]
           for f in glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
           if os.path.basename(f) != "__init__.py"]

mod_list = [__import__(mod, globals(), locals(), [], - 1) for mod in __all__]

pipes_dics = {}
for mod in mod_list:
    try:
        register = getattr(mod, "register")
    except:
        continue
    register(pipes_dics)

# validate pipes
for name, attr in pipes_dics.items():
    msg0 = "(pipe={}) ".format(name)

    def _check_attr(key):
        if key not in attr:
            msg = "'{}' attribute does not exsit.".format(key)
            raise InvalidPipeError(msg0 + msg)

    _check_attr("func")
    _check_attr("desc")
    _check_attr("args")

    def _check_type(key):
        args = attr[key]
        msg = "'{}' must be list of (str, dict)".format(key)
        if not isinstance(args, list):
            raise InvalidPipeError(msg0 + msg)
        for arg in args:
            try:  # arg.__getitem__() may fail
                if isinstance(arg[0], str) and isinstance(arg[1], dict):
                    continue
                raise TypeError
            except TypeError:
                raise InvalidPipeError(msg0 + msg)

    _check_type("args")
    if "kwds" in attr:
        _check_type("kwds")
