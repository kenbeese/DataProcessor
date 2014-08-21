# coding=utf-8

from .. import filter as flt


def register(pipes_dics):
    pipes_dics["filter_project"] = {
        "func": flt.project,
        "args": ["path"],
        "desc": "filter by project name",
    }
    pipes_dics["filter_node_type"] = {
        "func": flt.node_type,
        "args": ["node_type"],
        "desc": "filter by node type",
    }
