# coding=utf-8

from .exception import DataProcessorError
from .nodes import node_types
from . import utility


def project(node_list, path):
    """ Filter by project path.

    Parameters
    ----------
    path: str
        the path of project, whose children are left.
    """
    path = utility.path_expand(path)
    return [node for node in node_list if path in node["parents"]]


def node_type(node_list, ntype):
    """ Filter by node_type.

    Parameters
    ----------
    ntype: str
        nodes whose type is `ntype` are left in node_list.
    """
    if ntype not in node_types:
        raise DataProcessorError("Please select node type from "
                                 + str(node_types))
    return [node for node in node_list if node["type"] == ntype]
