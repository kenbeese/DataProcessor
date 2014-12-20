#!/usr/bin/env python
# coding=utf-8
"""API of web app."""

import os.path
import sys
import json
import traceback
from StringIO import StringIO
from contextlib import contextmanager
import cgitb
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
    with open("cfg.json") as f:
        cfg = json.load(f)
    data_path = cfg["data_path"]
    with dp.io.SyncDataHandler(data_path, duration=1, silent=True) as dh:
        dp.execute.execute(manip, dh.get())
    handler.operation_success()


@contextmanager
def print_capture():
    ss = StringIO()
    sys.stdout, ss = ss, sys.stdout
    try:
        yield sys.stdout
    finally:
        sys.stdout, ss = ss, sys.stdout


def pipe(req):
    """ Execute a manipulation s.t. [load, pipe, save].

    The pipe API do a single pipe to the data
    specified when the server stand.

    """
    with open("cfg.json") as f:
        cfg = json.load(f)
    data_path = cfg["data_path"]

    name = req.get("name")
    args = json.loads(req.get("args"))
    kwds = req.get("kwds") if req.has("kwds") else {}

    with dp.io.SyncDataHandler(data_path, silent=True) as dh:
        nl = dh.get()
        with print_capture() as ss:
            nl = dp.execute.pipe(name, args, kwds, nl)
            output_str = ss.getvalue()
        dh.update(nl)

    p = dp.pipes.pipes_dics[name]
    if "output" in p and p["output"] in ["json", "xml", "html"]:
        res = handler.Response(p["output"])
        res.set_body(output_str)
        print(res)
    else:
        handler.operation_success()


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
        with open("error.log", 'a+') as f:
            f.write(traceback.format_exc())
        handler.operation_fail("unknown error")
