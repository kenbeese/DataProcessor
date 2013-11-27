# coding=utf-8
"""Pipes of configure."""
import os.path
from ConfigParser import SafeConfigParser

from ..utility import read_configure


def add(node_list, filename, section="parameters"):
    """
    Add configure to node_list.

    Parameters
    ----------
    filename : str
        filename of parameter configure file
        If file is not exists, add null list.

    section : str
        Specify section name in configure file.

    Returns
    -------
    list
        node_list which is a list of dict.

    Examples
    --------
    >>> add(node_list, "configure.conf")
    >>> # Change load section.
    >>> add(node_list, "configure.conf", "defaults")

    """

    node_key = "configure"
    for node in node_list:
        confpath = os.path.join(node["path"], filename)
        conf_d = {}
        if os.path.exists(confpath):
            conf = SafeConfigParser()
            conf.optionxform = str
            conf.read(confpath)
            for key, var in conf.items(section):
                conf_d[key] = var
        else:
            Warning("parameter file is not exists.")
        if not node_key in node:
            node[node_key] = conf_d
        else:
            for key in conf_d:
                if key in node[node_key]:
                    Warning("overwrite configures")
            node[node_key].update(conf_d)

    return node_list


def no_section(node_list, filename, split_char="=", comment_char=["#"]):
    """
    Add configure to node_list.

    Parameters
    ----------
    filename : str
        filename of parameter configure file
        If file is not exists, add null list.
    split_char : str
        Specify the deliminator char.
    comment_char : str
        Specify the comment line signal char.

    Returns
    -------
    list
        node_list which is a list of dict.

    Examples
    --------
    >>> no_section(node_list, "foo.conf")
    >>> # Change deliminator and comment line signal
    >>> no_section(node_list, "foo.conf", split_char=":", comment_char="!")

    """

    for node in node_list:
        path = node["path"]
        cfg_path = os.path.join(path, filename)
        if not os.path.exists(cfg_path):
            continue
        cfg = read_configure(cfg_path, split_char, comment_char)
        if "configure" not in node:
            node["configure"] = {}
        node["configure"].update(cfg)
    return node_list


def register(pipes_dics):
    pipes_dics["configure"] = {
        "func": add,
        "args": ["filename"],
        "kwds": ["section"],
        "desc": "Read parameter file (use ConfigParser)",
    }
    pipes_dics["configure_no_section"] = {
        "func": no_section,
        "args": ["filename"],
        "kwds": ["split_char", "comment_char"],
        "desc": "Read parameter file (without section)",
    }
