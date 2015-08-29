# coding=utf-8

from ..nodes import remove
from ..basket import resolve_project_path


def remove_node(node_list, path):
    path = resolve_project_path(path)
    remove(node_list, path)
    return node_list


def register(pipe_dics):
    pipe_dics["remove_node"] = {
        "func": remove_node,
        "args": [("path", {"help": "path of node to be removed"}), ],
        "kwds": [],
        "desc": "Remove node from nodelist (does not remove data)"
    }
