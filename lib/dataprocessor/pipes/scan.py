# coding=utf-8
import os
from glob import glob

from ..nodes import get, validate_link
from ..utility import boolenize


def directory(node_list, root, whitelist, followlinks=False):
    """Scan nodes from all directories under the directory 'root'.

    Run node has one or more file or directory
    which satisfies node_dir/whitelist.
    Project node has run node in its sub-directory.

    Examples
    --------

    Initialize node_list.
    >>> node_list = directory([], "scandir_path", ["data/hoge*", "*foo*"])

    Rescan node_list.
    >>> node_list = [
    ...     {'path': '/tmp/scan_dir/run0',
    ...      'parents': [],   # empty
    ...      'children': [],  # empty
    ...      'name': 'run0',
    ...      'type': 'run'}]
    >>> node_list = directory([], "scandir_path", ["*.conf"])

    """

    root = os.path.abspath(os.path.expanduser(root))
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
        "args": ["root_path", "whitelist"],
        "desc": "scan direcoty structure",
    }
