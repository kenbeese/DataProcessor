# coding: utf-8

from .. import starter, utility
from ..runner import runners


def start(node_list, args, requirements=[],
          name=utility.now_str(), projects=[],
          runner="sync"):
    starter.start(node_list, args, requirements, name, projects, runner)
    return node_list


def register(pipes_dics):
    args = ("args", {
        "nargs": "+",
        "help": "arguments to execute"
    })
    requirements = ("requirements", {
        "nargs": "+",
        "help": "section parameters are written"
    })
    name = ("name", {
        "help": "name of new run"
    })
    projects = ("projects", {
        "nargs": "+",
        "help": "projects of new run"
    })
    runner = ("runner", {
        "choices": runners,
        "help": "runner"
    })
    pipes_dics["starter"] = {
        "func": start,
        "args": [args],
        "kwds": [requirements, name, projects, runner],
        "desc": "Start new run",
    }
