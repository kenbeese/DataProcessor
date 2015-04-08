# coding: utf-8

import os

from .. import nodes
from .. import utility
from . import add_tag


def add_run(node_list, path, tag=None, name=None, comment=""):
    """
    Add run node to node_list.

    Parameters
    ----------
    path : str
        Path of node.
    tag : str, optional
        Project name or project path. See "add_tag".
    name : str, optional
        Name of node. (default=basename of path)
    comment : str, optional
        Comment of node. (default="")

    """
    path = utility.abspath(path)
    utility.check_dir(path)
    if not name:
        name = os.path.basename(path)
    node = {"path": path,
            "name": name,
            "type": "run",
            "comment": comment,
            }
    node = nodes.normalize(node)
    nodes.add(node_list, node)
    if tag:
        node_list = add_tag.add_tag(node_list, path, tag)

    return node_list


def register(pipe_dics):
    pipe_dics["add_run"] = {
        "func": add_run,
        "args": ["path"],
        "kwds": ["tag", "name", "comment"],
        "desc": "Add run.",
    }
