# coding=utf-8
import json

from .exception import DataProcessorError, InvalidJSONError, pipe_execute
import pipes


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
    >>> manip = [{"nae": "save_json", "args": ["out.json"], "kwds": {"silent" : "True"}}]
    >>> try:
    ...     check_manip(manip) # typo: "nae"
    ... except InvalidJSONError as e:
    ...     print("[%s] %s" % (e.name, e.msg))
    [] pipe name is not defined
    >>> manip = [{"name": "save_json", "arg": ["out.json"], "kwds": {"silent" : "True"}}]
    >>> try:
    ...     check_manip(manip) # typo: "arg"
    ... except InvalidJSONError as e:
    ...     print("[%s] %s" % (e.name, e.msg))
    [save_json] attributes of pipes must be in 'name', 'args', 'kwds'
    >>> manip = [{"name": "save_json", "args": ["out.json"], "kwd": {"silent" : "True"}}]
    >>> try:
    ...     check_manip(manip) # typo: "kwd"
    ... except InvalidJSONError as e:
    ...     print("[%s] %s" % (e.name, e.msg))
    [save_json] attributes of pipes must be in 'name', 'args', 'kwds'
    >>> manip = [{"name": "sav_json", "args": ["out.json"], "kwds": {"silent" : "True"}}]
    >>> try:
    ...     check_manip(manip) # typo: "sav_json"
    ... except InvalidJSONError as e:
    ...     print("[%s] %s" % (e.name, e.msg))
    [sav_json] invalid pipe name
    >>> manip = [{"name": "save_json", "args": [], "kwds": {"silent" : "True"}}]
    >>> try:
    ...     check_manip(manip) # argument mismatch
    ... except InvalidJSONError as e:
    ...     print("[%s] %s" % (e.name, e.msg))
    [save_json] the number of arguments mismatches
    >>> manip = [{"name": "load_json", "args": ["in.json"], "kwds": {"silent": "True"}}]
    >>> try:
    ...     check_manip(manip) # `load_json` does not have "kwds"
    ... except InvalidJSONError as e:
    ...     print("[%s] %s" % (e.name, e.msg))
    [load_json] pipe does not have 'kwds'
    >>> manip = [{"name": "save_json", "args": ["out.json"], "kwds": {"silnt" : "True"}}]
    >>> try:
    ...     check_manip(manip) # typo in keywords: "silnt"
    ... except InvalidJSONError as e:
    ...     print("[%s] %s" % (e.name, e.msg))
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
            for kwd in mn["kwds"]:
                if kwd not in dic["kwds"]:
                    msg = "keyword argument '%s' does not exist"
                    raise InvalidJSONError(name, msg % kwd)
        else:
            mn["kwds"] = {}


def execute(manip):
    """execute pipeline defined in `manip`

    This function does not check whether `manip` is valid.
    Please check by `.check_manip`

    Parameters
    ----------
    manip : list
        A list defining manipulation
    """
    run_list = []
    for mn in manip:
        name = mn["name"]
        dic = pipes.pipes_dics[name]
        args = mn["args"]
        kwds = mn["kwds"]
        with pipe_execute(name):
            run_list = dic["func"](run_list, *args, **kwds)
    return run_list


def execute_from_json_str(manip_json_str):
    """execute pipeline from JSON string

    This do `check_manip` and `execute`.

    Raises
    ------
    InvalidJSONError
        It is raised if manipulation is invalid.
        See also `.check_manip`
    """
    try:
        manip = json.loads(manip_json_str)
    except ValueError:
        raise DataProcessorError("Cannot decode JSON file.")
    check_manip(manip)
    execute(manip)
