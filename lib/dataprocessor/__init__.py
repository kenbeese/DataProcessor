# coding=utf-8
import json
import traceback
from contextlib import contextmanager

import pipes


class DataProcessorError(Exception):
    """A runtime error occurred in DataProcessor

    This exception is raised when invalid manipulation is done.
    This exception will be caught in dataprocessor.execute,
    and converted into InvalidJSONError.

    Attribute
    ----------
    msg : str
        A message for the error
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class InvalidJSONError(Exception):
    """A runtime error occurred in processing manipulation

    Attribute
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


@contextmanager
def pipe_execute(name):
    try:
        yield
    except DataProcessorError as e:
        print(traceback.format_exc())
        raise InvalidJSONError(name, e.msg)


def execute(manip):
    """execute pipeline defined in `manip`

    Parameters
    ----------
    manip: list
        A list defining manipulation
    """
    run_list = []
    for mn in manip:
        name = mn["name"]
        if name not in pipes.pipes_dics:
            raise InvalidJSONError(name, "invalid pipe name")
        dic = pipes.pipes_dics[name]
        if len(mn["args"]) != len(dic["args"]):
            raise InvalidJSONError(name, "The number of arguments mismatches")
        if "kwds" in mn and "kwds" in dic:
            kwds = {}
            for kwd in mn["kwds"]:
                if kwd not in dic["kwds"]:
                    continue
                kwds[kwd] = mn["kwds"][kwd]
            with pipe_execute(name):
                run_list = dic["func"](run_list, *mn["args"], **kwds)
        else:
            with pipe_execute(name):
                run_list = dic["func"](run_list, *mn["args"])
    return run_list


def execute_from_json_str(manip_json_str):
    """execute pipeline from JSON string

    See also `dataprocessor.execute`.
    """
    manip = json.loads(manip_json_str)
    execute(manip)
