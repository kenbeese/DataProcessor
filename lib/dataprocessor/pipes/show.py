# coding=utf-8

from .. import filter as flt

default_format = "{path}"


def show_runs(node_list, project=None, show_format=default_format,
              parameters=[]):
    """ Show run list.

    Parameters
    ----------
    project : str or [str], optional
        the path of project, whose runs will be shown.
    show_format: str, optional
        specify format you want to output.
        You should use new `format` function format.
        This string will be formatted by `show_format.format(**node)`.
    parameters: [str], optional
        parameters to be displayed.

    Returns
    -------
    node_list

    """
    if project:
        runs = flt.project(node_list, project)
    else:
        runs = node_list
    runs = flt.node_type(runs, "run")
    for node in runs:
        cfg_str = ""
        if "configure" in node:
            for p in parameters:
                if p in node["configure"]:
                    cfg_str += " " + p + "=" + str(node["configure"][p])
        try:
            print(show_format.format(**node) + cfg_str)
        except:
            print(default_format.format(**node) + cfg_str)
    return node_list


def show_projects(node_list, show_format=default_format):
    """ Show project list.

    Parameters
    ----------
    show_format : str, optional
        specify format you want to output.
        You should use new `format` function format.
        This string will be formatted by `show_format.format(**node)`.

    Returns
    -------
    node_list

    """
    projects = flt.node_type(node_list, "project")
    for node in projects:
        try:
            print(show_format.format(**node))
        except:
            print(default_format.format(**node))
    return node_list


def register(pipe_dics):
    pipe_dics["show_runs"] = {
        "func": show_runs,
        "args": [],
        "kwds": ["project", "show_format"],
        "desc": "output runs path",
        "spec": [("parameters", {"nargs": "+",
                                 "help": "parameters to be displayed"})]
    }
    pipe_dics["show_projects"] = {
        "func": show_projects,
        "args": [],
        "kwds": ["show_format"],
        "desc": "output project name",
    }
