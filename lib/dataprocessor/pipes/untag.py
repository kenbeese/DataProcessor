# coding: utf-8
from ..nodes import get, add, remove
from ..utility import abspath
from ..rc import resolve_project_path
from ..exception import DataProcessorError


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
    project_path = resolve_project_path(project_id, False)

    node = get(node_list, path)
    if not node:
        raise DataProcessorError(
            "The path %s of node is not registered." % path)
    new_node = {}
    new_node.update(node)

    node = get(node_list, project_path)
    if not node:
        raise DataProcessorError(
            "The path %s of project is not registered." % project_path)
    new_project_node = {}
    new_project_node.update(node)

    if not project_path in new_node["parents"] or \
       not path in new_project_node["children"]:
        raise DataProcessorError("The tag %s is not specified." % project_id)
    new_node["parents"].remove(project_path)
    new_project_node["children"].remove(path)

    remove(node_list, path)
    remove(node_list, project_path)
    add(node_list, new_node)
    add(node_list, new_project_node)
    return node_list


def register(pipe_dics):
    pipe_dics["untag"] = {
        "func": untag,
        "args": ["path", "project_id"],
        "desc": "remove a tag from specified path",
    }
