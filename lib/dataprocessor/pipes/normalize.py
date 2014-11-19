# coding=utf-8
from .. import nodes


def normalize(node_list):
    new_nl = []
    for node in node_list:
        new_nl.append(nodes.normalize(node))
    return new_nl


def register(pipe_dics):
    pipe_dics["normalize"] = {
        "func": normalize,
        "args": [],
        "desc": "normalize nodes (i.e. fill necessary field)",
    }
