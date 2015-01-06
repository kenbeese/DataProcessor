# coding: utf-8

import json
import sys
import os.path
from StringIO import StringIO
from contextlib import contextmanager

from flask import Flask, request, render_template, Response

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
    data_path = app.config["DATA_PATH"]

    name = request.json["name"]
    args = json.loads(request.json["args"])
    kwds = request.json["kwds"] if "kwds" in request.json else {}

    with dp.io.SyncDataHandler(data_path, silent=True) as dh:
        nl = dh.get()
        with print_capture() as ss:
            nl = dp.execute.pipe(name, args, kwds, nl)
            output_str = ss.getvalue()
        dh.update(nl)

    p = dp.pipes.pipes_dics[name]
    if "output" in p and p["output"] in ["json", "xml", "html"]:
        return output_str
    return Response()
