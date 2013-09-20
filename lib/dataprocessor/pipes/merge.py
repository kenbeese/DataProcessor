# coding=utf-8

from . import jsonio
from .. import nodes


def merge(node_list, new_node_list, no_check=False):
    for node in new_node_list:
        nodes.add(node_list, node, no_check)
    return node_list


def merge_from_json(node_list, json_fn, no_check=False):
    new_node_list = []
    jsonio.load(new_node_list, json_fn)
    return merge(node_list, new_node_list, no_check)


def register(pipes_dics):
    pipes_dics["merge"] = {
        "func": merge,
        "args": ["new_node_list"],
        "kwds": ["no_check"],
        "desc": "merge node_list into existing one"
    }
    pipes_dics["merge_from_json"] = {
        "func": merge_from_json,
        "args": ["json_filename"],
        "kwds": ["no_check"],
        "desc": "merge node_list into existing one from JSON file"
    }
