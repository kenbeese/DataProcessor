# coding: utf-8
from ..nodes import get, add, remove
from ..utility import path_expand
from ..rc import resolve_project_path
from ..exception import DataProcessorError as dpError


def untag(node_list, path, project_id):
    """ Untag the node.

    Parameters
    ----------
    path : str
        Path of node.
    project_id : str
        the name or path of project.
        The path is resolved by resolve_project_path.

    Raises
    ------
    DataProcessorError
        raised when path of node or path specified
        by project id is not registered.

    """
    path = abspath(path)
    node = get(node_list, path)
    if not node:
        raise dpError("The path %s of node is not registered." % path)

    project_path = resolve_project_path(project_id, False)
    pnode = get(node_list, project_path)
    if not pnode:
        raise dpError("The path %s of project is not registered." % project_path)

    if project_path in node["parents"]:
        node["parents"].remove(project_path)
    if path in node["children"]:
        node["children"].remove(path)
    return node_list


def register(pipe_dics):
    pipe_dics["untag"] = {
        "func": untag,
        "args": ["path", "project_id"],
        "desc": "remove a tag from specified path",
    }
