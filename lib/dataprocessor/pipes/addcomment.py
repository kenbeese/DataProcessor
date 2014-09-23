# coding=utf-8
from ..nodes import get
from ..utility import path_expand
from ..exception import DataProcessorError


def add(node_list, comment, node_path):
    """
    Add comment to node spedcified path.

    Parameters
    ----------
    comment : str
        comment.

    node_path : str
        This path specify the unique node.

    Examples
    --------
    >>> node_list = [{"path": "/path/to/hoge"},
    ...              {"path": "/path/to/hogehoge"}]
    >>> add(node_list, "some comments", "/path/to/hoge") == [
    ...     {"path": "/path/to/hoge", "comment": "some comments"},
    ...     {"path": "/path/to/hogehoge"}]
    True
    >>> add(node_list, "some comments aho", "/path/to/hogehom")
    Traceback (most recent call last):
        ...
    DataProcessorError: 'There is no node with specified path: /path/to/hogehom'
    """
    path = path_expand(node_path)
    node = get(node_list, path)
    if node:
        node["comment"] = comment
    else:
        raise DataProcessorError("There is no node with specified path: %s"
                                 % path)
    return node_list


def register(pipe_dics):
    pipe_dics["add_comment"] = {
        "func": add,
        "args": ["comment", "path"],
        "desc": "add comment to node with path",
    }
