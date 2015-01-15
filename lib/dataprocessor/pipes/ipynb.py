# -*- coding: utf-8 -*-


import os.path as op
import webbrowser
from glob import glob
from .. import nodes
from .. import rc
from ..utility import path_expand, check_file
from ..ipynb import resolve_url, resolve_name
from ..exception import DataProcessorError as dpError


def start(nl, ipynb_path):
    """
    Start existing .ipynb file
    at standing ipython notebook server

    Parameters
    ----------
    ipynb_path : str
        path of existing .ipynb file

    Raise
    -----
    DataProcessorError
        - No IPython Notebook found
        - Existing notebook servers do not start
          on the parent directory of .ipynb file.
        - Cannot open browser

    """
    url = resolve_url(ipynb_path)
    try:
        webbrowser.open(url)
    except webbrowser.Error:
        raise dpError("Unknown error while opening notebook")
    return nl


def gather(node_list, pattern="*.ipynb"):
    """
    Search ipynb file by its extention
    """
    for node in node_list:
        path = node["path"]
        if not op.isdir(path):
            continue
        for fn in glob(op.join(path, pattern)):
            fn = path_expand(fn)
            node = {
                "path": fn,
                "type": "ipynb",
                "name": resolve_name(fn),
                "parents": [path, ],
                "children": [],
            }
            nodes.add(node_list, node, strategy="modest_update")
    return node_list


def add(node_list, path, parents=[]):
    """
    Add ipynb file manually
    """
    p = check_file(path)
    if isinstance(parents, str):
        parents = [parents]
    if not isinstance(parents, list):
        raise dpError("Parents must be a list")
    parents = map(lambda p: rc.resolve_project_path(p, False), parents)
    nodes.add(node_list, {
        "path": p,
        "type": "ipynb",
        "name": resolve_name(p),
        "parents": parents,
        "children": []
    }, strategy="modest_update")
    return node_list


def register(pipes_dics):
    pipes_dics["start_ipynb"] = {
        "func": start,
        "args": ["ipynb_path"],
        "desc": "start .ipynb in standing notebook",
    }
    pipes_dics["gather_ipynb"] = {
        "func": gather,
        "args": [],
        "desc": "gather ipynb files",
    }
    pipes_dics["add_ipynb"] = {
        "func": add,
        "args": [("path", {"help": "path of .ipynb file"})],
        "kwds": [("parents", {
            "help": "parents of new ipynb",
            "nargs": "+"
        })],
        "desc": "register .ipynb file"
    }
