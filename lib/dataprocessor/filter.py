# coding=utf-8

from .exception import DataProcessorError
from .nodes import node_types
from . import utility


def project(node_list, path):
    """ Filter by project path.
    """
    path = utility.path_expand(path)
    return [node for node in node_list if path in node["parents"]]


def node_type(node_list, ntype):
    """ Filter by node_type.
    """
    if ntype not in node_types:
        raise DataProcessorError("Please select node type from "
                                 + str(node_types))
    return [node for node in node_list if node["type"] == ntype]
