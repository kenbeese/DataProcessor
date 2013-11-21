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
from dataprocessor.exception import DataProcessorError
sys.path = [sys.path[0]] + sys.path[2:]


def _check(key, req):
    if key not in req.form:
        raise DataProcessorError("Request must include '%s'" % key)


def _get(key, req):
    _check(key, req)
    return req.form[key].value


def _load_json(val_str):
    try:
        val = json.loads(val_str)
    except ValueError:
        raise DataProcessorError("JSON is invalid")
    return val


def projects(req):
    with open("cfg.json") as f:
        cfg = json.load(f)
    data_path = cfg["data_path"]

    res_data = {
        "keys": ["name", "tags", "comment", "path"]
        }

    tbl = []
    with dp.io.DataHandler(data_path, silent=True) as dh:
        node_list = dh.get()
        for node in node_list:
            if node["type"] != "project":
                continue
            if "tags" not in node:
                node["tags"] = []
            if "comment" not in node:
                node["comment"] = ""
            tbl.append({
                "path": node["path"],
                "name": node["name"],
                "tags": node["tags"],
                "comment": node["comment"],
                })
    def mycmp(x,y):
        return cmp(x["name"], y["name"])
    tbl.sort(mycmp)
    res_data["table"] = tbl

    res = handler.Response("json")
    res.set_body(json.dumps(res_data))
    print(res)


def widgets(req):
    path = _get("path", req)
    table_type = _get("table_type", req)

    with open("cfg.json") as f:
        cfg = json.load(f)
    data_path = cfg["data_path"]

    groups=[
            {'items': ['comment', 'tags'], 'name': 'node'},
            {'dict_path': ['configure']},
            ]
    with dp.io.DataHandler(data_path, silent=True) as dh:
        node_list = dh.get()
        node = dp.nodes.get(node_list, path)
        tbl = dp.table.Table(node, node_list, table_type, groups)
        html_str = tbl.render()

    res = handler.Response("json")
    res.set_body(json.dumps([html_str,]))
    print(res)

def switch():
    req = handler.Request()
    _check("type", req)
    types = {"Projects": projects, "Widgets": widgets}
    t = req.form["type"].value
    if t not in types:
        raise DataProcessorError("'type' must be in the followings: "
                                 + (" ".join(types.keys())))
    types[t](req)


if __name__ == "__main__":
    try:
        switch()
    except DataProcessorError as e:
        handler.operation_fail(e.msg)
