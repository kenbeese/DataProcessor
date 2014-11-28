# coding=utf-8
from ..nodes import get, add
from ..utility import path_expand
from ..rc import get_project_dir
from ..exception import DataProcessorError

import os.path


def add_project(node_list, node_path, project_name):
    """
    Add comment to node spedcified path.

    Parameters
    ----------
    project_name : str
        comment.
    node_path : str
        This path specify the unique node.

    """
    path = path_expand(node_path)
    project_path = get_project_dir(project_name)
    project_node = get(node_list, project_path)
    if not project_node:
        add(node_list, {
            "path": project_path,
            "type": "project",
            "name": os.path.basename(project_path),
            "children": [path],
            "parents": [],
        })
    else:
        if path not in project_node["children"]:
            project_node["children"].append(path)
    node = get(node_list, path)
    if not node:
        raise DataProcessorError("There is no node (path=%s)." % path)
    if project_path not in node["parents"]:
        node["parents"].append(project_path)
    return node_list


def register(pipe_dics):
    pipe_dics["add_project"] = {
        "func": add_project,
        "args": ["path", "project_name"],
        "desc": "add project",
    }
