# coding: utf-8

import sys
import os.path
from StringIO import StringIO
from contextlib import contextmanager

from flask import Flask, request, render_template, Response, abort

sys.path = ([sys.path[0]]
            + [os.path.join(os.path.dirname(__file__), "../lib")]
            + sys.path[1:])
import dataprocessor as dp
sys.path = [sys.path[0]] + sys.path[2:]


app = Flask(__name__)


@contextmanager
def print_capture():
    ss = StringIO()
    sys.stdout, ss = ss, sys.stdout
    try:
        yield sys.stdout
    finally:
        sys.stdout, ss = ss, sys.stdout


@app.route('/')
def show_layout():
    return render_template('layout.html')


@app.route('/api/pipe', methods=['POST'])
def execute_pipe():

    def _execute_pipe():
        with dp.io.SyncDataHandler(data_path, silent=True) as dh:
            nl = dh.get()
            with print_capture() as ss:
                nl = dp.execute.pipe(name, args, kwds, nl)
                output_str = ss.getvalue()
            dh.update(nl)
        return output_str

    def _handle_json(req):
        name = req.json["name"]
        args = req.json["args"]
        kwds = req.json["kwds"] if "kwds" in req.json else {}
        return name, args, kwds

    data_path = app.config["DATA_PATH"]

    try:
        name, args, kwds = _handle_json(request)
    except KeyError as key:
        app.logger.error("Request must include {}".format(key))
        abort(400)

    try:
        p = dp.pipes.pipes_dics[name]
    except KeyError as key:
        app.logger.error("The pipe {} is not found".format(key))
        abort(400)

    try:
        output_str = _execute_pipe()
    except dp.exception.DataProcessorError as e:
        app.logger.error(e.msg)
        abort(400)

    if "output" in p and p["output"] in ["json", "xml", "html"]:
        return output_str
    else:
        return Response()
