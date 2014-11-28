# coding=utf-8
"""Configure manager of dataprocessor
"""

from . import utility, io
from .exception import DataProcessorError
import os.path
import copy
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
        val = get_configure(rc_section, name, rcpath)
        parser.add_argument("--" + name, default=val, **opt)
    parser.add_argument("--debug", action="store_true",
                        help="output traceback")
    return parser


def load_into_argparse(parser, section_name, options, allow_empty=False,
                       rcpath=default_rcpath):
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
            val = get_configure(section_name, name, rcpath)
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


def load(rcpath=default_rcpath):
    """Load node_list from default data.json.

    Parameters
    ----------
    rcpath : str, optional
        path of configure file (default=~/.dataprocessor.ini)

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
    parser = get_configparser(rcpath)
    if not parser.has_option(rc_section, "json"):
        raise DataProcessorRcError("Configure does not contains JSON path.")
    return io.load([], parser.get(rc_section, "json"))


def update(node_list, rcpath=default_rcpath):
    """Save node_list into default data.json with update strategy.

    Parameters
    ----------
    rcpath : str, optional
        path of configure file (default=~/.dataprocessor.ini)

    Raises
    ------
    DataProcessorRcError
        raised when

        - configure file does not exist.
        - configure file does not contain JSON path

    """
    parser = get_configparser(rcpath)
    if parser.has_option(rc_section, "json"):
        raise DataProcessorRcError("Configure does not contains JSON path.")
    with io.SyncDataHandler(parser.get(rc_section, "json"), silent=True) as dh:
        dh.update(node_list)


def get_configparser(rcpath=default_rcpath):
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


def get_configure(section, key, rcpath=default_rcpath):
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
    cfg = get_configparser(rcpath)
    if not cfg.has_option(section, key):
        raise DataProcessorRcError("Configure not found (section:{}, key:{}))"
                                   .format(section, key))
    return cfg.get(section, key)


def _get_dir(name, root, basket_name, rcpath):
    if not root:
        root = get_configure(rc_section, "root", rcpath=rcpath)
    root = utility.check_directory(root)
    basket = utility.get_directory(os.path.join(root, basket_name))
    return utility.get_directory(os.path.join(basket, name))


def get_project_dir(name, root=None, basket_name="Projects",
                    rcpath=default_rcpath):
    """ Generate project directory, if it exists, returns its abspath.

    Parameters
    ----------
    name : str
        project name (not path)
    root : str, optional
        new run directory is made in `${root}/${basket_name}/`.
        If not specified, "root" value of the setting file is used.
    basket_name : str, optional
        new run directory is made in `${root}/${basket_name}/`.
        (default="Projects")
    rcpath : str, optional
        path of the setting file

    Raises
    ------
    DataProcessorRcError
        occurs when `root` is not specified and it cannot be loaded
        from the setting file.

    """
    if os.path.basename(name) == name:
        return _get_dir(name, root, basket_name, rcpath)
    else:
        return utility.get_directory(name)
