# coding=utf-8

import os.path as op
from .. import pipe, configure
from ..utility import abspath, check_file
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

    cfg = configure.parse(ft, confpath, section=section)

    if configure.node_key not in node:
        node[configure.node_key] = {}
    node[configure.node_key].update(cfg)
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
