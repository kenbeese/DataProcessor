# coding=utf-8

import os.path as op
from .. import pipe, configure
from ..utility import read_configure, abspath, check_file
from ..exception import DataProcessorError as dpError


@pipe.type("run")
def load(node, filename, filetype=None, section="parameters"):
    """ Load configure

    Parameters
    ----------
    filename : str
        filename of parameter configure file
        If file does not exist, add null list.
    section : str
        Specify section name in configure file.

    Examples
    --------
    >>> load(node_list, "configure.conf") # doctest:+SKIP
    >>> # Change load section.
    >>> load(node_list, "configure.conf", "defaults") # doctest:+SKIP

    """
    confpath = abspath(op.join(node["path"], filename))
    check_file(confpath)

    ft = configure.string_to_filetype(filetype)
    if ft is configure.FileType.NONE:
        ft = configure.guess_filetype_from_path(confpath)
    if ft is configure.FileType.NONE:
        raise dpError("Cannot determine filetype of configure file.")

    cfg = configure.parse(ft, confpath, section)

    if configure.node_key not in node:
        node[configure.node_key] = {}
    node[configure.node_key].update(cfg)
    return node


@pipe.type("run")
def no_section(node, filename, split_char="=", comment_char=["#"]):
    """ Load configure

    Parameters
    ----------
    filename : str
        filename of parameter configure file
        If file does not exist, add null list.
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
    return node


def register(pipes_dics):
    pipes_dics["configure"] = {
        "func": load,
        "args": ["filename"],
        "kwds": [("section", {"help": "section parameters are written"}),
                 ("filetype", {"help": "filetype [ini, yaml]. If not given, "
                                       "determined automatically by the "
                                       "filename extension."})],
        "desc": "Read parameter file (use ConfigParser)",
    }
    pipes_dics["configure_no_section"] = {
        "func": no_section,
        "args": ["filename"],
        "kwds": [
            ("split_char", {"help": "separetor of parameters"}),
            ("comment_char", {"help": "charactors defines comment line"})
        ],
        "desc": "Read parameter file (without section)",
    }
