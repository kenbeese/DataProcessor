# coding=utf-8

import enum
import os
import yaml
import ConfigParser as cp
from logging import getLogger, NullHandler
from .exception import DataProcessorError as dpError

logger = getLogger(__name__)
logger.addHandler(NullHandler())


_filetype_list = ["ini", "yaml", "nosection"]
FileType = enum.Enum("FileType", "NONE " + " ".join(_filetype_list))
node_key = "configure"


def guess_filetype_from_path(path):
    """
    Get filetype from path (filename extension).

    Parameters
    ----------
    path: str
        path to a file

    Returns
    -------
    FileType enum

    """
    _, ext = os.path.splitext(path)

    # check extension in case insensitive way
    ext = ext.lower()
    if ext in (".ini", ".conf"):
        return FileType.ini
    elif ext in (".yml", ".yaml"):
        return FileType.yaml
    else:
        logger.warning("Unknown extension '{}'".format(ext))
        return FileType.NONE


def string_to_filetype(filetype_str):
    """
    Convert string to FileType.

    Parameters
    ----------
    filetype_str: str
        name of FileType

    Returns
    -------
    FileType enum

    """
    if not filetype_str:
        logger.debug("Empty filetype")
        return FileType.NONE
    try:
        return FileType[filetype_str.lower()]
    except KeyError:
        logger.warning("Invalid filetype : " + filetype_str)
        return FileType.NONE


def parse_ini(confpath, section="defaults", **kwds):
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


def parse_nosection(confpath, split_char="=", comment_char=["#"], **kwds):
    """ Read configure file without sections.

    Parameters
    ----------
    confpath : str
        The file name of the configure file
    split_char : str, optional
        The lines in configure file are splited by this char (default "=").
        If your configure has line s.t. `a : 1.2`,
        then you should set `split_char=":"`.
    comment_char : list of str, optional
        The line starting with chars in this list will be skipped.
        (default=["#"])

    Returns
    -------
    dict

    """
    config = {}
    with open(confpath, "r") as f:
        for i, line in enumerate(f):
            if line[0] in comment_char or line == "\n":
                continue
            lines = line.strip().split(split_char)
            if(len(lines) != 2):
                logger.debug("Invalid line {path}:{i} {line}".format(path=confpath, i=i, line=line))
                continue
            config[lines[0].strip()] = lines[1].strip()
    return config


def parse_yaml(confpath, section="parameters", **kwds):
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
    elif filetype == FileType.nosection:
        return parse_nosection
    else:
        raise dpError("Unsupported filetype: {}".format(filetype))


def parse(filetype, path, **kwds):
    """
    Parse configure file

    Parameters
    ----------
    filetype : FileType
        see enum filetype.FileType
    confpath : str
        Path to config file.
    section : str
        Specify section name in configure file.

    Returns
    -------
    dict

    """
    parser = get_parser(filetype)
    return parser(path, **kwds)
