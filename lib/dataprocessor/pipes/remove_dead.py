# coding=utf-8

import os.path as op
from .. import nodes


def remove_dead(nodelist):
    """ Remove nodes that no longer exist.
    """
    paths = [node["path"] for node in nodelist]
    for path in paths:
        if not op.exists(path):
            nodes.remove(nodelist, path)
    return nodelist


def register(pipes_dics):
    pipes_dics["remove_dead"] = {
        "func": remove_dead,
        "args": [],
        "desc": "Remove nodes that no longer exist.",
    }
