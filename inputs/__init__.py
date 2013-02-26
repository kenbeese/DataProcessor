"""@package DataProcessor.input
"""

__all__ = ["DirConstructor"]


input_dics = {}

from . import DirConstructor

DirConstructor.register(input_dics)
