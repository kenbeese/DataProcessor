# -*- coding: utf-8 -*-


import sys
from functools import wraps
from .nodes import node_types
from .filter import node_type as type_filter
from .exception import DataProcessorError as dpError


def type(typename):
    if typename not in node_types:
        raise dpError("invalid type name")

    def decorator(func):
        @wraps(func)
        def wrapper(node_list, *args, **kwds):
            for node in type_filter(node_list, typename):
                try:
                    func(node, *args, **kwds)
                except dpError as e:
                    print >>sys.stderr, e
                    continue
            return node_list
        return wrapper
    return decorator
