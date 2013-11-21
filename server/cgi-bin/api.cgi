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


def _check(key, req):
    if key not in req.form:
        raise DataProcessorError("Request must include '%s'" % key)


def _load_json(val_str):
    try:
        val = json.loads(val_str)
    except ValueError:
        raise DataProcessorError("JSON is invalid")
    return val


def manip(req):
    _check("manip", req)
    manip = _load_json(req.form["manip"].value)
    dp.execute.check_manip(manip)
    dp.execute.execute(manip)


def pipe(req):
    raise DataProcessorError("API 'pipe' has not been implemented yet.")


def switch():
    req = handler.Request()
    _check("type", req)
    types = {"manip": manip, "pipe": pipe, }
    t = req.form["type"].value
    if t not in types:
        raise DataProcessorError("'type' must be in the followings: "
                                 + (" ".join(types.keys())))
    types[t](req)


if __name__ == "__main__":
    try:
        switch()
        handler.operation_success()
    except InvalidJSONError as e:
        message = "ERROR occurs in pipe '%s'; %s" % (e.name, e.msg)
        handler.operation_fail(message)
    except DataProcessorError as e:
        handler.operation_fail(e.msg)
    except Exception:
        handler.operation_fail("unknown error")
