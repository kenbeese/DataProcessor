# coding=utf-8
from ..nodes import get, add
from ..utility import abspath
from ..rc import resolve_project_path
from ..exception import DataProcessorError

import os.path


def add_tag(node_list, node_path, project_id):
    """ Make the node belong to the project specified by project id.

    We realize "tagging" feature by project nodes.

    Parameters
    ----------
    node_path : str
        This path specify the unique node.
    project_id: str
        the name or path of project.
        The path is resolved by resolve_project_path.

    """
    path = abspath(node_path)
    project_path = resolve_project_path(project_id, True)
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
    pipe_dics["add_tag"] = {
        "func": add_tag,
        "args": ["path", "project_id"],
        "desc": "Add a tag into the node",
    }
