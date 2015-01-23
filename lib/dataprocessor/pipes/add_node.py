# coding=utf-8

import os.path
from .. import nodes
from .. import utility


def add_node(node_list, path=".", node_type="run", children=[],
             name=None, parents=[".."], strategy="raise"):
    """Add node.

    A node is added to the node_list.

    Parameters
    ----------
    path : str, optional
        path of node (default=".")
    node_type : str, optional {"run", "project"}
        type of node (default="run")
    name : str, optional
    children : list, optional
    parents : list, optional
    strategy : str, optional
        determines how to deal with conflict,
        i.e. there alread exists another node
        whose path is same as new one.
        See docstring of nodes.add.

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

    node = nodes.normalize({
        "path": path,
        "type": node_type,
        "children": [utility.path_expand(c_path) for c_path in children],
        "parents": [utility.path_expand(c_path) for c_path in parents],
        "name": name
    })
    nodes.add(node_list, node, strategy=strategy)
    return node_list


def register(pipes_dics):
    pipes_dics["add_node"] = {
        "func": add_node,
        "args": [],
        "kwds": [
            ("path", {"help": "path of new node"}),
            ("name", {"help": "name of new node"}),
            ("node_type", {
                "help": "type of new node",
                "choices": nodes.node_types,
            }),
            ("children", {"help": "children paths of new node"}),
            ("parents", {"help": "paths parents of new node"}),
            ("strategy", {
                "help": "strategy for resolving conflict",
                "choices": ["raise", "update", "modest_update", "replace"],
            }),
        ],
        "desc": "Add node to node_list."
    }
