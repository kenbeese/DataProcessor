#!/usr/bin/python
# coding=utf-8

import os.path
import sys
import cgitb
import json
cgitb.enable()

sys.path = ([sys.path[0]]
            + [os.path.join(os.path.dirname(__file__), "../../lib")]
            + sys.path[1:])
import dataprocessor as dp
import handler
from dataprocessor.exception import DataProcessorError, InvalidJSONError
sys.path = [sys.path[0]] + sys.path[2:]


def manip(req):
    """ Do a full manipulation. """
    manip = json.loads(req.get("manip"))
    dp.execute.check_manip(manip)
    dp.execute.execute(manip)


def pipe(req):
    """ Execute a manipulation s.t. [load, pipe, save].

    The pipe API do a single pipe to the data
    specified when the server stand.

    """
    if req.has("kwds"):
        pipe = {
            "name": req.get("name"),
            "args": json.loads(req.get("args")),
            "kwds": json.loads(req.get("kwds"))
        }
    else:
        pipe = {
            "name": req.get("name"),
            "args": json.loads(req.get("args")),
        }

    with open("cfg.json") as f:
        cfg = json.load(f)
    data_path = cfg["data_path"]

    pipe_load = {"name": "load_json", "args": [data_path, ], }
    pipe_save = {
        "name": "save_json",
        "args": [data_path, ],
        "kwds": {"silent": True},
    }
    manip = [pipe_load, pipe, pipe_save]
    dp.execute.check_manip(manip)
    dp.execute.execute(manip)


def switch():
    """ Switch two APIs {manip, pipe}. """
    req = handler.Request()
    types = {"manip": manip, "pipe": pipe, }
    t = req.get("type")
    if t not in types:
        raise DataProcessorError("'type' must be in the followings: "
                                 + (" ".join(types.keys())))
    types[t](req)


if __name__ == "__main__":
    try:
        switch()
        handler.operation_success()
    except KeyError as key:
        handler.operation_fail("Request must include '%s'" % key)
    except ValueError:
        handler.operation_fail("JSON is invalid")
    except InvalidJSONError as e:
        message = "ERROR occurs in pipe '%s'; %s" % (e.name, e.msg)
        handler.operation_fail(message)
    except DataProcessorError as e:
        handler.operation_fail(e.msg)
    except Exception:
        handler.operation_fail("unknown error")
