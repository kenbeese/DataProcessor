# coding=utf-8
"""Configure manager of dataprocessor
"""

from . import utility, io
from .exception import DataProcessorError
import os
import copy
import argparse
import ConfigParser


if "DP_DEBUG_RCPATH" in os.environ and os.environ["DP_DEBUG_RCPATH"]:
    default_rcpath = utility.abspath(os.environ["DP_DEBUG_RCPATH"])
else:
    default_rcpath = "~/.dataprocessor.ini"
rc_section = "data"


class DataProcessorRcError(DataProcessorError):

    """Exception about configure file."""

    def __init__(self, msg):
        DataProcessorError.__init__(self, msg)


def ArgumentParser(options={}):
    """Argument parser for executables in this project.

    Parameters
    ----------
    options : [{str: dict}], optional
        options which you want to read from [data] section
        of the configure file.
        `[{"opt1": argparse_opt}]` will converted into
        `parser.add_argument("--" + "opt1", **argparse_opt)`.

    Returns
    -------
    argparse.ArgumentParser

    Raises
    ------
    DataProcessorRcError
        raised when

        - configure file does not exist.
        - configure file does not contain specified values

    """
    parser = argparse.ArgumentParser()
    if "json" not in options:
        options["json"] = {"help": "path of JSON file"}
    for name, opt in options.items():
        val = get_configure(rc_section, name)
        parser.add_argument("--" + name, default=val, **opt)
    parser.add_argument("--debug", action="store_true",
                        help="output traceback nad debug message")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="output INFO log")
    return parser


def load_into_argparse(parser, section_name, options, allow_empty=False):
    """ Load configure into argparse.

    Parameters
    ----------
    parser : argparse.ArgumentParser
        main parser or subparser

    section_name : str
        name of section

    options : {str: {str: str}}
        Options which you want to read from section
        whose name is `section_name`.
        `[{"opt1": argparse_opt}]` will converted into
        `parser.add_argument("--" + "opt1", **argparse_opt)`.

    """
    for name, opt in options.items():
        opt = copy.deepcopy(opt)
        try:
            val = get_configure(section_name, name)
            opt["default"] = val
        except DataProcessorRcError:
            if not allow_empty:
                raise
            if "default" not in opt:
                parser.add_argument(name, **opt)
                continue
        if "help" in opt:
            opt["help"] += " (default={})".format(str(opt["default"]))
        else:
            opt["help"] = "(default={})".format(str(opt["default"]))
        parser.add_argument("--" + name, **opt)


def load():
    """Load node_list from default data.json.

    Returns
    -------
    node_list

    Raises
    ------
    DataProcessorRcError
        raised when

        - configure file does not exist.
        - configure file does not contain JSON path

    """
    parser = get_configparser()
    if not parser.has_option(rc_section, "json"):
        raise DataProcessorRcError("Configure does not contains JSON path.")
    return io.load([], parser.get(rc_section, "json"))


def update(node_list):
    """Save node_list into default data.json with update strategy.

    Raises
    ------
    DataProcessorRcError
        raised when

        - configure file does not exist.
        - configure file does not contain JSON path

    """
    parser = get_configparser()
    if parser.has_option(rc_section, "json"):
        raise DataProcessorRcError("Configure does not contains JSON path.")
    with io.SyncDataHandler(parser.get(rc_section, "json")) as dh:
        dh.update(node_list)


def get_configparser():
    """ Get configure parser

    Returns
    -------
    ConfigParser.SafeConfigParser
        configure file has been loaded.

    Raises
    ------
    DataProcessorRcError
        raised when configure file does not exist.

    """
    rcpath = utility.abspath(default_rcpath)
    if not os.path.exists(rcpath):
        raise DataProcessorRcError(
            "Configure file does not exist at {}".format(rcpath))

    parser = ConfigParser.SafeConfigParser()
    parser.read(rcpath)
    return parser


def get_configure(section, key):
    """ Get configure value

    Parameters
    ----------
    section : str
        section name of configure file

    key : str
        key of configure

    Returns
    -------
    str
        configure value

    Raises
    ------
    DataProcessorRcError
        raised when

        - configure file does not exist.
        - configure file does not contain specified values

    """
    cfg = get_configparser()
    if not cfg.has_option(section, key):
        raise DataProcessorRcError("Configure not found (section:{}, key:{}))"
                                   .format(section, key))
    return cfg.get(section, key)


def get_configure_safe(section, key, default):
    """ Get configure value safely.

    Parameters
    ----------
    section : str
        section name of configure file
    key : str
        key of configure
    default : any
        This is returned in the case where configure cannot be obtained.

    Returns
    -------
    str
        configure value
    """
    try:
        return get_configure(section, key)
    except DataProcessorRcError:
        return default


def _check_and_create_dir_abspath(path):
    path = utility.abspath(path)
    utility.check_or_create_dir(path)
    return path


def create_configure_file(rcpath, root_dir, json_path):
    """
    Create a configure file and a json.

    If the json file does not exist, the file is created.

    Parameters
    ----------
    rcpath : str
        path of configure file
    rootdir : str
        path of data root directory
    jsonpath : str
        path of data json

    """
    rcpath = utility.abspath(rcpath)

    if not os.path.exists(json_path):
        with open(json_path, "w") as f:
            f.write("[]")

    cfg = ConfigParser.RawConfigParser()
    cfg.add_section(rc_section)
    cfg.set(rc_section, "root", root_dir)
    cfg.set(rc_section, "json", json_path)

    with open(rcpath, 'wb') as f:
        cfg.write(f)
