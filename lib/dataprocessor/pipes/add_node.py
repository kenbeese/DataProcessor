# coding=utf-8

import os.path
from .. import nodes
from .. import utility


def add_node(node_list, path=".", node_type="run", children=[],
             name=None, parents=[".."]):
    """Add node.

    A node is added to the node_list according to dict.update.

    Parameters
    ----------
    path : str, optional
        path of node (default=".")
    node_type : str, optional {"run", "project"}
        type of node (default="run")
    name : str, optional
    children : list, optional
    parents : list, optional

    Returns
    -------
    node_list

    """
    path = utility.path_expand(path)

    if isinstance(children, str):
        children = [children]
    if isinstance(parents, str):
        parents = [parents]
    if not name:
        name = os.path.basename(path)

    node = {"path": path, "type": node_type,
            "children": [utility.path_expand(c_path) for c_path in children],
            "parents": [utility.path_expand(c_path) for c_path in parents],
            "name": name}
    nodes.add(node_list, node, strategy="modest_update")
    return node_list


def register(pipes_dics):
    pipes_dics["add_node"] = {
        "func": add_node,
        "args": [],
        "kwds": ["path", "node_type", "children", "name", "parents"],
        "desc": "Add node to node_list."
    }
