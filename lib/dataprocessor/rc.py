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


def get_configure_safe(section, key, default, rcpath=default_rcpath):
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
        return get_configure(section, key, rcpath)
    except DataProcessorRcError:
        return default


def _resolve_path(name, create_dir, root, basket_name, rcpath):
    if not root:
        root = get_configure(rc_section, "root", rcpath=rcpath)
    root = utility.check_directory(root)
    if create_dir:
        basket = utility.get_directory(os.path.join(root, basket_name))
        return utility.get_directory(os.path.join(basket, name))
    else:
        basket = utility.check_directory(os.path.join(root, basket_name))
        return utility.ceck_directory(os.path.join(basket, name))


def resolve_project_path(name_or_path, create_dir, root=None,
                         basket_name=get_configure_safe(rc_section,
                                                        "project_basket",
                                                        "Projects"),
                         rcpath=default_rcpath):
    """ Resolve project path from its path or name.

    Parameters
    ----------
    name_or_path : str
        Project identifier.
        If name (i.e. basename(name_or_path) == name_or_path),
        abspath of `root/basket_name/name` is returned.
        If path (otherwise case), returns its abspath.
    create_dir : boolean
        This flag determine the behavior occured when there is no directory at
        the resolved path as follows:
        - if create_dir is True: create new directory
        - if create_dir is False: raise DataProcessorError
    root : str, optional
        The root path of baskets. (default=None)
        If None, the path is read from the configure file.
    basket_name : str, optional
        The name of the project basket.
        If "project_basket" is specified in the configure file,
        default value is it. Otherwise, default is "Projects".
    rcpath : str, optional
        path of the setting file

    Returns
    -------
    path : str
        existing project path

    Raises
    ------
    DataProcessorRcError
        occurs when `root` is not specified and it cannot be loaded
        from the setting file.

    DataProcessorError
        occurs when create_dir is False and a path is not resolved.

    """
    if os.path.basename(name_or_path) == name_or_path:
        return _resolve_path(name_or_path, create_dir, root, basket_name, rcpath)
    else:
        if create_dir:
            return utility.get_directory(name_or_path)
        else:
            return utility.check_directory(name_or_path)