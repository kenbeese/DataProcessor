# coding=utf-8
"""@package DataProcessor
"""


__all__ = ["processor", "pipes", "inputs", "outputs", "libs"]

input_dics = {}

def input_sample(args):
    run_list = [
            {"path":"/home/username/data/P1/run1"},
            {"path":"/home/username/data/P1/run2"},
        ]
    return run_list

input_dics["sample"] = {
    "name" : "sample",
    "args" : [],
    "func" : input_sample
    }
