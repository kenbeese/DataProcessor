# -*- coding: utf-8 -*-

from .. import runner, pipe, basket
from .. import filter as dpfilter


@pipe.directory
def foreach_dir(node, args):
    runner.sync(args, node["path"])
    return node


@pipe.type("run")
def _foreach_run(node, args):
    runner.sync(args, node["path"])
    return node


def foreach_run(node_list, args, project=None):
    if project:
        node_list = dpfilter.project(node_list, basket.resolve_project_path(project))
    return _foreach_run(node_list, args)


@pipe.type("project")
def foreach_project(node, args):
    runner.sync(args, node["path"])
    return node


def register(pipes_dics):
    args = ("args", {
        "nargs": "+",
        "help": "command (use '--' when you use option, e.g. foreach -- ls -lt)",
    })
    project = ("project", {
        "help": "project name or path",
    })
    pipes_dics["foreach"] = {
        "func": foreach_dir,
        "args": [args],
        "desc": "Execute a command in all managed directories",
    }
    pipes_dics["foreach_run"] = {
        "func": foreach_run,
        "args": [args],
        "kwds": [project],
        "desc": "Execute a command in run directories",
    }
    pipes_dics["foreach_project"] = {
        "func": foreach_project,
        "args": [args],
        "desc": "Execute a command in project directories",
    }
