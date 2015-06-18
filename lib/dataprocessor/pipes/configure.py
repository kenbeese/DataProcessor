# coding=utf-8

import sys
import os.path as op
import yaml
import ConfigParser as cp

from .. import pipe
from ..utility import read_configure, check_file
from ..exception import DataProcessorError as dpError
from ..filetype import FileType
from ..filetype import guess_filetype_from_path as guess_ft


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
    conf = cp.SafeConfigParser()
    conf.optionxform = str
    try:
        read_conf = conf.read(confpath)
    except cp.MissingSectionHeaderError:
        raise dpError("Invalid INI file: " + confpath)
    if not read_conf:
        raise dpError("Cannot read INI configure file: " + confpath)
    try:
        return dict(conf.items(section))
    except cp.NoSectionError:
        raise dpError("Section does not found: " + confpath)


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
        try:
            d = yaml.load(f)
        except yaml.YAMLError:
            raise dpError("Fail to parse YAML file : " + confpath)
    if section not in d:
        raise dpError("No such section '{}' in {}".format(section, confpath))
    return d[section]


def get_parser(filetype):
    """
    Get parser corresponding to the filetype
    Parameters
    ----------
    filetype : FileType
        see enum filetype.FileType
    Returns
    -------
    function that takes 2 args, confpath and section.
    """
    # check extension in case insensitive way
    if filetype == FileType.ini:
        return parse_ini
    elif filetype == FileType.yaml:
        return parse_yaml
    else:
        return None


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
    NODE_KEY = "configure"

    confpath = check_file(op.join(node["path"], filename))
    ft = FileType.NONE

    if filetype:
        try:
            ft = FileType[filetype.lower()] 
        except KeyError:
            print >>sys.stderr, "Invalid filetype : " + filetype
            print >>sys.stderr, "Guess from extention"
            ft = guess_ft(confpath)
    else:
        ft = guess_ft(confpath)

    print ft
    # Invalid filetype
    if ft == FileType.NONE:
        raise dpError("File type error.")

    parser = get_parser(ft)
    cfg = parser(confpath, section)

    if NODE_KEY not in node:
        node[NODE_KEY] = {}
    node[NODE_KEY].update(cfg)
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
