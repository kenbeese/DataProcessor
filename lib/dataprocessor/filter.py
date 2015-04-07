# coding=utf-8

from .exception import DataProcessorError
from .nodes import node_types
from . import utility
from .basket import resolve_project_path


def project(node_list, path):
    """ Filter by project path.

    Parameters
    ----------
    path : str or [str]
        the path of project (or projects), whose children are left.

    Raises
    ------
    DataProcessorError
        If path is not specified by str or [str].

    Returns
    -------
    node_list

    """
    if isinstance(path, str):
        paths = [resolve_project_path(path, False)]
    elif isinstance(path, list):
        paths = [resolve_project_path(p, False) for p in path]
    else:
        raise DataProcessorError("Arguemnt path must be str or [str]")
    return [node for node in node_list
            if not set(paths).isdisjoint(node["parents"])]


def node_type(node_list, ntype):
    """ Filter by node_type.

    Parameters
    ----------
    ntype : str
        nodes whose type is `ntype` are left in node_list.

    Raises
    ------
    DataProcessorError
        If specified ntype is not supported.

    Returns
    -------
    node_list

    """
    if ntype not in node_types:
        raise DataProcessorError("Please select node type from "
                                 + str(node_types))
    return [node for node in node_list if node["type"] == ntype]


def prefix_path(node_list, pre_path):
    """Filter by prefix path.

    In the case when pre_path is "/foo/bar",
    following paths remain (not filtered):

    - /foo/bar
    - /foo/bar/foo

    , and following do not remain (filtered out):

    - /foo/barfoo/hoge
    - /bar/foo/bar/FOO

    Parameters
    ----------
    pre_path : str
        prefix path for filtering.

    Returns
    -------
    node_list

    """
    p = utility.abspath(pre_path)
    length = len(p)
    return [node for node in node_list
            if node["path"] == p or node["path"][0:length + 1] == p + "/"]
