# coding=utf-8
"""Configure manager of dataprocessor
"""

from . import utility, io
from .exception import DataProcessorError
import os.path
import argparse
import ConfigParser


default_rcpath = "~/.dataprocessor.ini"
rc_section = "data"


class DataProcessorRcError(DataProcessorError):
    """Exception about configure file."""
    def __init__(self, msg):
        DataProcessorError.__init__(self, msg)


def ArgumentParser(rcpath=default_rcpath, options={}):
    """Argument parser for executables in this project.

    Parameters
    ----------
    rcpath : str, optional
        path of configure file (default=~/.dataprocessor.ini)

    options : dict, optional
        This option enables you to add another options
        in addition to "json". Additional option behaves as
        "json" option. See the usage of `dpmanip`.
        You should read the code to use this option.

    Returns
    -------
    argparse.ArgumentParser

    """
    parser = argparse.ArgumentParser()
    options["json"] = {"help": "path of JSON file"}
    try:
        cfg = get_parser(rcpath)
        for name, opt in options.items():
            if cfg.has_option(rc_section, name):
                val = cfg.get(rc_section, name)
                parser.add_argument("--" + name, default=val, **opt)
            else:
                parser.add_argument(name, **opt)
    except DataProcessorRcError:
        for name, opt in options.items():
            parser.add_argument(name, **opt)
    parser.add_argument("--debug", action="store_true",
                        help="output traceback")
    return parser


def load(rcpath=default_rcpath):
    """Load node_list from default data.json.

    Parameters
    ----------
    rcpath : str, optional
        path of configure file (default=~/.dataprocessor.ini)

    Returns
    -------
    node_list

    """
    parser = get_parser(rcpath)
    if parser.has_option(rc_section, "json"):
        raise DataProcessorRcError("Configure does not contains JSON path.")
    return io.load([], parser.get(rc_section, "json"))


def update(node_list, rcpath=default_rcpath):
    """Save node_list into default data.json with update strategy.

    Parameters
    ----------
    rcpath : str, optional
        path of configure file (default=~/.dataprocessor.ini)

    """
    parser = get_parser(rcpath)
    if parser.has_option(rc_section, "json"):
        raise DataProcessorRcError("Configure does not contains JSON path.")
    with io.SyncDataHandler(parser.get(rc_section, "json"), silent=True) as dh:
        dh.update(node_list)


def get_parser(rcpath=default_rcpath):
    """ Get configure parser

    Parameters
    ----------
    rcpath : str, optional
        path of configure file (default=~/.dataprocessor.ini)

    Returns
    -------
    ConfigParser.SafeConfigParser
        configure file has been loaded.

    Raises
    ------
    DataProcessorRcError
        raised when configure file does not exist.

    """
    rcpath = utility.path_expand(rcpath)
    if not os.path.exists(rcpath):
        raise DataProcessorRcError("Configure file does not exist")

    parser = ConfigParser.SafeConfigParser()
    parser.read(rcpath)
    return parser
