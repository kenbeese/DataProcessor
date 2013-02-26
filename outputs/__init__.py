# coding=utf-8
"""@package DataProcessor.output
"""


__all__ == ["csv"]


output_dics = {}


from . import csv
csv.register(output_dic)
