# coding=utf-8
import json

from .exception import DataProcessorError, InvalidJSONError, pipe_execute
import pipes


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

    Raises
    ------
    DataProcessorError
        If fails to decode JSON.
    """
    try:
        manip = json.loads(manip_json_str)
    except ValueError:
        raise DataProcessorError("Cannot decode JSON file.")
    execute(manip)
