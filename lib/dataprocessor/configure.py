# coding=utf-8

import enum
import os
import yaml
import ConfigParser as cp
from logging import getLogger, NullHandler
from .exception import DataProcessorError as dpError

logger = getLogger(__name__)
logger.addHandler(NullHandler())


_filetype_list = ["ini", "yaml"]
FileType = enum.Enum("FileType", "NONE " + " ".join(_filetype_list))


def guess_filetype_from_path(path):
    """
    Get filetype from path (filename extension).

    Parameters
    ----------
    path: str
        path to a file

    Returns
    -------
    FileType enum. If unknown filename extension is given, show warning
    """
    _, ext = os.path.splitext(path)

    # check extension in case insensitive way
    ext = ext.lower()
    if ext in (".ini", ".conf"):
        return FileType.ini
    elif ext in (".yml", ".yaml"):
        return FileType.yaml
    else:
        logger.warnings("Unknown ext '{}'".format(ext))
        return FileType.NONE


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
        raise dpError("Invalid filetype: {}".format(filetype))
