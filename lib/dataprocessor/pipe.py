# -*- coding: utf-8 -*-

"""
This module provides wrapper functions
which make easy to define a SIMD-like pipe,
i.e. operates independently on each nodes.

The following two codes are equal without error handling:

>>> @wrap
... def pipe1(node, arg1, kwd1=""):
...     print(node)
...     node["attr1"] = "val"
...     return node

>>> def pipe1(node_list, arg1, kwd1=""):
...     for node in node_list:
...         print(node)
...         node["attr1"] = "val"
...     return node_list

Error handling policy is following:

- If ``DataProcessorError`` or its inherited is raised
  in the decorated function while processing a node,
  this process is quited and continue with another nodes.

- If another exception is raised,
  whole processes are quited.

Simply, corresponds to the following conceptual code:

>>> for node in node_list:
...     try:
...         decorated(node)
...     except DataProcessorError:
...         continue

"""

import sys
import os.path as op
from functools import wraps

from .nodes import node_types
from .exception import DataProcessorError as dpError


class PipeImplementationError(Exception):

    """
    Raised when the implementation of pipe is invalid

    Attributes
    ----------
    name : str
        The name of pipe in which error occurred.
    msg : str
        A message for the error

    """

    def __init__(self, name, msg):
        self.name = name
        self.msg = msg

    def __str__(self):
        return "[%s]: %s" % (self.name, self.msg)


def _wrap(filter_func):
    def decorator(func):
        @wraps(func)
        def wrapper(node_list, *args, **kwds):
            for node in node_list:
                if not filter_func(node):
                    continue
                try:
                    new_node = func(node, *args, **kwds)
                    if not isinstance(new_node, dict):
                        raise PipeImplementationError(func.__name__,
                                                      "Pipe must return node")
                    if new_node and new_node != node:
                        node.clear()
                        node.update(new_node)
                except dpError as e:
                    print >>sys.stderr, e
                    continue
            return node_list
        return wrapper
    return decorator


wrap = _wrap(lambda _: True)
wrap.__doc__ = """
    Create a pipe from a function operates on a node.

    This decorator makes easy to define a SIMD-like pipe,
    i.e. operates independently on each nodes.

    Examples
    --------
    The following two codes are equal without error handling:

    >>> @wrap
    ... def pipe1(node, arg1, kwd1=""):
    ...     print(node)
    ...     node["attr1"] = "val"
    ...     return node

    >>> def pipe1(node_list, arg1, kwd1=""):
    ...     for node in node_list:
    ...         print(node)
    ...         node["attr1"] = "val"
    ...     return node_list

    """


file = _wrap(lambda n: op.isfile(n["path"]))
file.__doc__ = "Create a pipe which operates on file nodes"


directory = _wrap(lambda n: op.isdir(n["path"]))
directory.__doc__ = "Create a pipe which operates on directory nodes"


def type(typename):
    """ Create a pipe which operates on nodes of specific type.

    Examples
    --------

    >>> nl = [{
    ...     "path": "/path/1",
    ...     "type": "project",
    ...     "children": ["/path/2"],
    ...     "parents": [],
    ... }, {
    ...     "path": "/path/2",
    ...     "type": "run",
    ...     "children": [],
    ...     "parents": ["/path/1"],
    ... }]
    >>> @type("run")
    ... def run_pipe(node):
    ...     node["comment"] = "RUN"
    ...     return node
    >>> @type("project")
    ... def project_pipe(node):
    ...     node["comment"] = "PROJECT"
    ...     return node
    >>> nl = run_pipe(nl)
    >>> nl = project_pipe(nl)
    >>> nl == [{
    ...     "path": "/path/1",
    ...     "type": "project",
    ...     "children": ["/path/2"],
    ...     "parents": [],
    ...     "comment": "PROJECT",
    ... }, {
    ...     "path": "/path/2",
    ...     "type": "run",
    ...     "children": [],
    ...     "parents": ["/path/1"],
    ...     "comment": "RUN",
    ... }]
    True

    works on project nodes only.

    """
    if typename not in node_types:
        raise dpError("Invalid type name: {}".format(typename))
    return _wrap(lambda n: n["type"] == typename)
