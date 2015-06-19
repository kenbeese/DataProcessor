# coding=utf-8
"""dataprocessor
"""
import glob
import os.path
from . import pipes, tests

__all__ = [os.path.basename(f)[:-3]
           for f in glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
           if os.path.basename(f) != "__init__.py"]

mod_list = [__import__(mod, globals(), locals(), [], - 1) for mod in __all__]
