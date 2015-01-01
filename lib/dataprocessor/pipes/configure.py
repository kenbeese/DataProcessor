# coding=utf-8

import os.path as op
import yaml
from ConfigParser import SafeConfigParser

from .. import pipe
from ..utility import read_configure, check_file
from ..exception import DataProcessorError as dpError


def parse_ini(confpath, section):
    """
    Parse .ini and .conf to dictionary

    Parameters
    ----------
    confpath : str
        Path to config file.
    section : str
        Specify section name in configure file.

    Returns
    -------
    Specified section as a dictionary.
    """
    conf = SafeConfigParser()
    conf.optionxform = str
    conf.read(confpath)
    return dict(conf.items(section))


def parse_yaml(confpath, section):
    """
    Parse .yaml to dictionary

    Parameters
    ----------
    confpath : str
        Path to config file.
    section : str
        Specify section name in configure file.

    Returns
    -------
    Specified section as a dictionary.
    """
    with open(confpath, "r") as f:
        d = yaml.load(f)
    if section not in d:
        raise dpError("No such section '{}' in {}".format(section, confpath))
    return d[section]

parsers = {
    "ini": parse_ini,
    "yaml": parse_yaml,
}


def get_filetype(path):
    """
    Get filetype from path (filename extension).

    Parameters
    ----------
    path: str
        path to a file

    Returns
    -------
    filetype as a string.
    """
    _, ext = op.splitext(path)

    # check extension in case insensitive way
    ext = ext.lower()
    if ext in (".ini", ".conf"):
        return "ini"
    elif ext in (".yml", ".yaml"):
        return "yaml"
    else:
        raise dpError("Unknown filename extension ({})".format(ext))


@pipe.type("run")
def add(node, filename, filetype=None, section="parameters"):
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
    >>> add(node_list, "configure.conf") # doctest:+SKIP
    >>> # Change load section.
    >>> add(node_list, "configure.conf", "defaults") # doctest:+SKIP

    """
    confpath = check_file(op.join(node["path"], filename))
    if not filetype or filetype not in parsers:
        filetype = get_filetype(confpath)
    cfg = parsers[filetype](confpath, section)

    if "configure" not in node:
        node["configure"] = {}
    node["configure"].update(cfg)
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
        "func": add,
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
        "kwds": ["split_char", "comment_char"],
        "desc": "Read parameter file (without section)",
    }
