# coding=utf-8
from .. import nodes, utility


def change_name(node_list, path, name):

    path = utility.path_expand(path)
    node = nodes.get(node_list, path)
    node["name"] = name
    return node_list


def register(pipes_dics):
    pipes_dics["change_name"] = {
        "func": change_name,
        "args": [("path", {"help": "path"}),
                 ("name", {"help": "new name"})
                 ],
        "desc": "Change name."
    }
