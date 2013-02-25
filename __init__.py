# coding=utf-8

"""DataProcessor
"""

__all__ = ["filters","processor"]

input_dic = {}
output_dic = {}

def input_sample(args):
    run_list = [
            {"path":"/home/username/data/P1/run1"},
            {"path":"/home/username/data/P1/run2"},
        ]
    return run_list

input_dic["sample"] = {
    "name" : "sample",
    "args" : [],
    "func" : input_sample
    }
