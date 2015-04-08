# coding=utf-8
import os
import shutil
import copy
from ..exception import DataProcessorError
from ..nodes import change_path
from ..utility import abspath
from ..filter import prefix_path


def move_node(node_list, from_path, dest):
    """
    Move node like as UNIX mv.

    Change path of a node and related nodes.
    Coresponding directories are also moved or renamed.

    Parameters
    ----------
    from_path : str
        path of node.
    dest : str
        path of destination.

    Return
    ------
    node_list

    Raises
    ------
    DataProcessorError
        raised when path of 'dest' already exists and the path is a file.

    """
    def resolve_destination(dest):
        # move and rename
        if not os.path.exists(dest):
            return dest
        # move to directory
        if os.path.isdir(dest):
            return os.path.join(dest, os.path.basename(from_path))
        raise DataProcessorError(
            "The destinaition %s already exists." % dest)

    from_path = abspath(from_path)
    dest = abspath(dest)  # for move function
    to_path = resolve_destination(dest)  # for node_list
    work_nl = copy.deepcopy(node_list)

    if os.path.isfile(from_path):
        work_nl = change_path(work_nl, from_path, to_path, silent=True)
        shutil.move(from_path, dest)

    if os.path.isdir(from_path):
        target_nodes = prefix_path(work_nl, from_path)
        for node in target_nodes:
            to_p = node["path"].replace(from_path, to_path, 1)
            work_nl = change_path(work_nl, node["path"], to_p, silent=True)
        shutil.move(from_path, dest)

    node_list = work_nl
    return node_list


def register(pipe_dics):
    pipe_dics["move_node"] = {
        "func": move_node,
        "args": ["from_path", "dest"],
        "kwds": [],
        "desc": "move node whose directory is also moved like as UNIX mv"
    }
    pipe_dics["change_path"] = {
        "func": change_path,
        "args": ["from_path", "to_path"],
        "kwds": ["silent"],
        "desc": "change path of node",
    }
