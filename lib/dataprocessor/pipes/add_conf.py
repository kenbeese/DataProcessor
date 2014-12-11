# coding: utf-8

from .. import utility
from .. import nodes
from .. import exception


def add_conf(node_list, path, key, value):
    """
    Add a new configure to the specified node.

    Parameters
    ----------
    path : str
        Specify the node.
    key : str
        key of configure.
    value : str
        value of configure.

    """
    conf_key = "configure"
    path = utility.path_expand(path)
    node = nodes.get(node_list, path)
    nodes.remove(node_list, path)
    node = nodes.normalize(node)
    if node:
        node[conf_key][key] = value
    else:
        raise exception.DataProcessorError(
            "Tha path %s is not registered." % path)
    nodes.add(node_list, node)
    return node_list


def register(pipes_dics):
    pipes_dics["add_conf"] = {
        "func": add_conf,
        "args": ["path", "key", "value"],
        "desc": "Add a new configure to the path.",
    }
