# coding=utf-8
import json

from .exception import DataProcessorError, InvalidJSONError, pipe_execute
from . import pipes


def check_manip(manip):
    """ check whether maniplation is valid

    Parameters
    ----------
    manip : list
        A list defining manipulation

    Raises
    ------
    InvalidJSONError
        It is raised if manipulation is invalid.

    Examples
    --------
    >>> def do_check_manip(manip):
    ...     try:
    ...         check_manip(manip)
    ...     except InvalidJSONError as e:
    ...         print("[%s] %s" % (e.name, e.msg))
    >>> do_check_manip([{"nae": "save_json", # typo: "nae"
    ...                  "args": ["out.json"],
    ...                  "kwds": {"silent" : "True"}}])
    [] pipe name is not defined
    >>> do_check_manip([{"name": "save_json",
    ...                  "arg": ["out.json"], # typo: "arg"
    ...                  "kwds": {"silent" : "True"}}])
    [save_json] attributes of pipes must be in 'name', 'args', 'kwds'
    >>> do_check_manip([{"name": "save_json",
    ...                  "args": ["out.json"],
    ...                  "kwd": {"silent" : "True"}}]) # typo: "kwd"
    [save_json] attributes of pipes must be in 'name', 'args', 'kwds'
    >>> do_check_manip([{"name": "sav_json", # typo: "sav_json"
    ...                  "args": ["out.json"],
    ...                  "kwds": {"silent" : "True"}}])
    [sav_json] invalid pipe name
    >>> do_check_manip([{"name": "save_json",
    ...                  "args": [], # argument mismatch
    ...                  "kwds": {"silent" : "True"}}])
    [save_json] the number of arguments mismatches
    >>> do_check_manip([{"name": "load_json",
    ...                  "args": ["in.json"],
    ...                  "kwds": {"silent": "True"}}])
    ...                  # `load_json` does not have "kwds"
    [load_json] pipe does not have 'kwds'
    >>> do_check_manip([{"name": "save_json",
    ...                  "args": ["out.json"],
    ...                  "kwds": {"silnt" : "True"}}])
    ...                  # typo in keywords: "silnt"
    [save_json] keyword argument 'silnt' does not exist
    """
    for mn in manip:
        if "name" not in mn:
            raise InvalidJSONError("", "pipe name is not defined")
        name = mn["name"]
        for k in mn:
            if k not in ["name", "args", "kwds"]:
                msg = "attributes of pipes must be in 'name', 'args', 'kwds'"
                raise InvalidJSONError(name, msg)
        if name not in pipes.pipes_dics:
            raise InvalidJSONError(name, "invalid pipe name")
        dic = pipes.pipes_dics[name]
        if len(mn["args"]) != len(dic["args"]):
            raise InvalidJSONError(name, "the number of arguments mismatches")
        if "kwds" in mn:
            if "kwds" not in dic:
                raise InvalidJSONError(name, "pipe does not have 'kwds'")
            kwd_names = [kwd for kwd, _ in dic["kwds"]]
            for kwd in mn["kwds"]:
                if kwd not in kwd_names:
                    msg = "keyword argument '%s' does not exist"
                    raise InvalidJSONError(name, msg % kwd)
        else:
            mn["kwds"] = {}


def execute(manip, node_list=[]):
    """execute pipeline defined in `manip`

    This function does not check whether `manip` is valid.
    Please check by `.check_manip`

    Parameters
    ----------
    manip : list
        A list defining manipulation
    node_list : list, optional
        initial node_list (default=[])

    Returns
    -------
    node_list : list
    """
    for mn in manip:
        name = mn["name"]
        dic = pipes.pipes_dics[name]
        args = mn["args"]
        kwds = mn["kwds"]
        with pipe_execute(name):
            node_list = dic["func"](node_list, *args, **kwds)
    return node_list


def execute_from_json_str(manip_json_str, node_list=[]):
    """execute pipeline from JSON string

    This do `check_manip` and `execute`.

    Raises
    ------
    InvalidJSONError
        It is raised if manipulation is invalid.
        See also `.check_manip`

    Returns
    -------
    node_list : list
    """
    try:
        manip = json.loads(manip_json_str)
    except ValueError:
        raise DataProcessorError("Cannot decode JSON file.")
    check_manip(manip)
    return execute(manip, node_list)
