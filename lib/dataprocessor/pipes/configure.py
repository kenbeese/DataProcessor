# coding=utf-8

import os.path as op
from ConfigParser import SafeConfigParser

from .. import pipe
from ..utility import read_configure, check_file
from ..exception import DataProcessorError as dpError


@pipe.type("run")
def add(node, filename, section="parameters"):
    """ Load configure

    Parameters
    ----------
    filename : str
        filename of parameter configure file
        If file is not exists, add null list.
    section : str
        Specify section name in configure file.

    Examples
    --------
    >>> add(node_list, "configure.conf") # doctest:+SKIP
    >>> # Change load section.
    >>> add(node_list, "configure.conf", "defaults") # doctest:+SKIP

    """
    confpath = check_file(op.join(node["path"], filename))

    conf = SafeConfigParser()
    conf.optionxform = str
    conf.read(confpath)

    if "configure" not in node:
        node["configure"] = {}
    node["configure"].update(dict(conf.items(section)))


@pipe.type("run")
def no_section(node, filename, split_char="=", comment_char=["#"]):
    """ Load configure

    Parameters
    ----------
    filename : str
        filename of parameter configure file
        If file is not exists, add null list.
    split_char : str
        Specify the deliminator char.
    comment_char : str
        Specify the comment line signal char.

    Examples
    --------
    >>> no_section(node_list, "foo.conf") # doctest:+SKIP
    >>> # Change deliminator and comment line signal
    >>> no_section(node_list, "foo.conf", split_char=":", comment_char="!")
    ... # doctest:+SKIP

    """
    path = node["path"]
    cfg_path = check_file(op.join(path, filename))
    cfg = read_configure(cfg_path, split_char, comment_char)
    if "configure" not in node:
        node["configure"] = {}
    node["configure"].update(cfg)


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
