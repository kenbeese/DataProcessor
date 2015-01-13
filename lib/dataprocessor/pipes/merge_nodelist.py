# coding=utf-8

import json

from .. import nodes
from .. import utility


def merge_nodelist(node_list, json_filename):
    """ Merge another node_list.

    Parameters
    ----------
    json_fn : str
        filename of JSON file including another node_list
    """
    fn = utility.check_file(json_filename)
    with open(fn) as f:
        another_nl = json.load(f)
    for node in another_nl:
        nodes.add(node_list, node,
                  strategy="modest_update",
                  skip_validate_link=True)
    for node in node_list:
        nodes.validate_link(node_list, node, silent=True)
    return node_list


def register(pipes_dics):
    pipes_dics["merge_nodelist"] = {
        "func": merge_nodelist,
        "args": [("json_filename", {
            "help": "path of another JSON file"
        })],
        "kwds": [],
        "desc": "Merge another node_list",
    }
