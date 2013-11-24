# coding=utf-8
import os.path
from .. import figure


def register(pipe_dics):
    pipe_dics["register_figure"] = {
        "func": figure.register,
        "args": ["figures", "figure_directory"],
        "kwds": ["runs", "generators"],
        "desc": "add figure node into node_list",
    }
