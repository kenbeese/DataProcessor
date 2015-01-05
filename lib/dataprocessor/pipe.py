# -*- coding: utf-8 -*-

import sys
import os.path as op
from functools import wraps

from .nodes import node_types
from .exception import DataProcessorError as dpError


def _wrap(filter_func):
    def decorator(func):
        @wraps(func)
        def wrapper(node_list, *args, **kwds):
            for node in node_list:
                if not filter_func(node):
                    continue
                try:
                    new_node = func(node, *args, **kwds)
                    if new_node != node:
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

    >>> def pipe1(node_list, arg1, kwd1=""):
    ...     for node in node_list:
    ...         print(node)

    """


file = _wrap(lambda n: op.isfile(n["path"]))
file.__doc__ = "Create a pipe which operates on file nodes"


directory = _wrap(lambda n: op.isdir(n["path"]))
directory.__doc__ = "Create a pipe which operates on directory nodes"


def type(typename):
    """ Create a pipe which operates on nodes of specific type.

    Examples
    --------

    >>> @type("run")
    ... def pipe1(node):
    ...     pass

    works on run nodes only, and

    >>> @type("project")
    ... def pipe2(node):
    ...     pass

    works on project nodes only.

    """
    if typename not in node_types:
        raise dpError("Invalid type name: {}".format(typename))
    return _wrap(lambda n: n["type"] == typename)
