# coding=utf-8

from .. import utility
from .. import filter as flt

default_format = "{path}"


def show(node_list, show_format=default_format):
    """ Show node with specified format.
    """
    for node in node_list:
        print(show_format.format(**node))


def show_runs(node_list, project=None, show_format=default_format):
    """ Show run list.
    """
    if project:
        project = utility.path_expand(project)
        runs = flt.project(node_list, project)
    else:
        runs = node_list
    runs = flt.node_type(runs, "run")
    show(runs, show_format)
    return node_list


def show_projects(node_list, show_format=default_format):
    """ Show project list.
    """
    projects = flt.node_type(node_list, "project")
    show(projects, show_format)
    return node_list


def register(pipe_dics):
    pipe_dics["show_runs"] = {
        "func": show_runs,
        "args": [],
        "kwds": ["project", "show_format"],
        "desc": "output runs path",
    }
    pipe_dics["show_projects"] = {
        "func": show_projects,
        "args": [],
        "kwds": ["show_format"],
        "desc": "output project name",
    }
