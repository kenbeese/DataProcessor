# coding=utf-8
"""Scan directories as nodes."""
import os
from glob import glob

from ..nodes import get, validate_link
from ..utility import path_expand, boolenize


def directory(node_list, root, whitelist, followlinks=False):
    """Scan nodes from all directories under the directory 'root'.

    If one directory has properties of both of 'run' and 'project',
    type of the directory is set to 'run'.

    Parameters
    ----------
    root : str
        Scan directories recursively under the directory `root`.
    whitelist : list of str
        Run node has one or more file or directory
        which satisfies run_node_dir/`whitelist`.
        And project nodes satisfy project_dir/run_node_dir/`whitelist`.
        str can be specified by wildcard.
    followlinks : {'False', 'True'}, optional
        Whether scan in symbolic link.
        Be aware that setting this to True may lead to infinite recursion.

    Returns
    -------
    node_list

    Examples
    --------
    >>> # Initialize node_list.
    >>> node_list = directory([], "scandir_path", ["data/hoge*", "*foo*"])

    >>> # Rescan node_list.
    >>> node_list = [
    ...     {'path': '/tmp/scan_dir/run0',
    ...      'parents': [],   # empty
    ...      'children': [],  # empty
    ...      'name': 'run0',
    ...      'type': 'run'}]
    >>> node_list = directory([], "scandir_path", ["*.conf"])

    """

    root = path_expand(root)
    followlinks = boolenize(followlinks)
    scan_nodelist = []
    for path, dirs, files in os.walk(root, followlinks=followlinks):
        dirs.sort()
        node_type = None
        parents = []
        children = []
        if not get(node_list, path) is None:
            continue
        for child in dirs:
            for white in whitelist:
                if glob(os.path.join(path, child, white)):
                    node_type = "project"
                    children.append(os.path.join(path, child))
                    break
        for white in whitelist:
            if glob(os.path.join(path, white)):
                node_type = "run"
                parents.append(os.path.dirname(path))
                break
        if not node_type:
            continue
        scan_nodelist.append({"path": path,
                              "parents": parents,
                              "children": children,
                              "type": node_type,
                              "name": os.path.basename(path),
                              })
    origin_len = len(node_list)
    node_list = node_list + scan_nodelist
    for node in node_list[origin_len:]:
        validate_link(node_list, node, silent=True)
    return node_list


def register(pipe_dics):
    pipe_dics["scan_directory"] = {
        "func": directory,
        "args": ["root", "whitelist"],
        "kwds": ["followlinks"],
        "desc": "Scan nodes from all directories under the directory 'root'.",
    }
