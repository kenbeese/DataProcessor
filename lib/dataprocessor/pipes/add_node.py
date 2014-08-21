# coding=utf-8

import os.path
from .. import nodes
from .. import utility


def add_node(node_list, path=".", node_type="run", children=[],
             name=None, parents=[".."]):
    """Add node.

    Parameters
    ----------
    path : str, optional
        default is set to ".".
    node_type : str, optional
        default is set to "run"
    name : str, optional
    children : list, optional
    parents : list, optional

    Return
    ------
    node_list

    """
    path = utility.path_expand(path)

    if isinstance(children, str):
        children = [children]
    if isinstance(parents, str):
        parents = [parents]
    name = os.path.basename(path)
    node = {"path": path, "type": node_type,
            "children": [utility.path_expand(c_path) for c_path in children],
            "parents": [utility.path_expand(c_path) for c_path in parents],
            "name": name}
    nodes.add(node_list, node)
    return node_list


def register(pipes_dics):
    pipes_dics["add_node"] = {
        "func": add_node,
        "args": [],
        "kwds": ["path", "node_type", "children", "name", "parents"],
        "desc": "Add node to node_list."
    }
