# coding: utf-8

import sys
import os
import os.path
import time
import copy

from flask import Flask, request, render_template, Response, abort, \
    redirect, url_for, g, flash, session

sys.path = ([sys.path[0]]
            + [os.path.join(os.path.dirname(__file__), "../lib")]
            + sys.path[1:])
import dataprocessor as dp
sys.path = [sys.path[0]] + sys.path[2:]


app = Flask(__name__)


@app.before_request
def before_request():
    g.data_path = app.config["DATA_PATH"]


@app.route('/')
def show_projectlist():
    with dp.io.SyncDataHandler(g.data_path, silent=True) as dh:
        nl = dh.get()
    projects = dp.filter.node_type(nl, "project")
    return render_template('projectlist.html', projects=projects)


@app.route('/ipynblist')
def show_ipynblist():
    nl = dp.io.load([], g.data_path)
    ipynb = dp.filter.node_type(nl, "ipynb")
    nb = dp.ipynb.gather_notebooks()
    for n in ipynb:
        p = n["path"]
        try:
            n["url"] = dp.ipynb.resolve_url(p, nb)
        except dp.exception.DataProcessorError:
            n["url"] = ""
        n["name"] = dp.ipynb.resolve_name(p)
        n["mtime"] = os.stat(p).st_mtime
        n["mtime_str"] = time.strftime("%Y/%m/%d-%H:%M:%S",
                                       time.localtime(n["mtime"]))
    # for tag
    ipynb = copy.deepcopy(ipynb)
    for n in ipynb:
        n["tag-nodes"] = []
        for p in n["parents"]:
            n["tag-nodes"].append(dp.nodes.get(nl, p))

    return render_template(
        "ipynblist.html",
        ipynb=sorted(ipynb, key=lambda n: n["mtime"], reverse=True),
    )


@app.route('/node/<path:path>')
def show_node(path):
    path = "/" + path
    with dp.io.SyncDataHandler(g.data_path, silent=True) as dh:
        nl = dh.get()

    node = dp.nodes.get(nl, path)

    show_function = {"run": show_run, "project": show_project}
    return show_function[node["type"]](node, nl)


def show_run(node, node_list):

    # for tag
    parent_nodes = []
    for p in node["parents"]:
        parent_nodes.append(dp.nodes.get(node_list, p))

    # for completion of add tag
    project_id_nodes = dp.filter.prefix_path(
        node_list, dp.rc.resolve_project_path(""))
    project_ids = [n["name"] for n in project_id_nodes]

    # for ipynb
    ipynb_nodes = []
    for p in node["children"]:
        n = dp.nodes.get(node_list, p).copy()
        if n["type"] != "ipynb":
            continue
        try:
            n["url"] = dp.ipynb.resolve_url(p)
        except dp.exception.DataProcessorError:
            n["url"] = ""
        n["name"] = dp.ipynb.resolve_name(p)
        ipynb_nodes.append(n)

    return render_template("run.html", node=node, ipynb=ipynb_nodes,
                           parents=parent_nodes, project_ids=project_ids)


def show_project(node, node_list):
    df = dp.dataframe.get_project(node_list, node["path"],
                                  properties=["comment"]).fillna("")

    # for tag
    parent_nodes = []
    for p in node["parents"]:
        parent_nodes.append(dp.nodes.get(node_list, p))

    # for completion of add tag
    project_id_nodes = dp.filter.prefix_path(
        node_list, dp.rc.resolve_project_path("", False))
    project_ids = [n["name"] for n in project_id_nodes]

    def _count_uniq(col):
        return len(set(df[col]))
    index = sorted(df.columns, key=_count_uniq, reverse=True)
    cfg = [c for c in index if c not in ["name", "comment"]]
    return render_template("project.html", df=df, cfg=cfg, node=node,
                           parents=parent_nodes, project_ids=project_ids)


@app.route('/api/pipe', methods=['POST'])
def execute_pipe():

    def _parse_req(req):
        name = req.json["name"]
        args = req.json["args"]
        kwds = req.json["kwds"] if "kwds" in req.json else {}
        return name, args, kwds

    try:
        name, args, kwds = _parse_req(request)
        _execute_pipe(g.data_path, name, args, kwds)
    except KeyError as key:
        app.logger.error("Request must include {}".format(key))
        abort(400)
    except dp.exception.DataProcessorError as e:
        app.logger.error(e.msg)
        abort(400)
    return Response()


def _execute_pipe(data_path, name, args, kwds):
    with dp.io.SyncDataHandler(data_path, silent=True) as dh:
        nl = dh.get()
        nl = dp.execute.pipe(name, args, kwds, nl)
        dh.update(nl)


@app.route('/add_tag/<path:path>', methods=['POST'])
def add_tag(path):
    session['logged_in'] = True
    if request.form['tagname'] == "":
        flash("Specify tagname")
        return redirect(url_for('show_node', path=path))
    else:
        flash("Added tag '{}'".format(request.form['tagname']))
        _execute_pipe(g.data_path,
                      "add_tag", ["/" + path, request.form['tagname']], {})
        return redirect(url_for('show_node', path=path))


@app.route('/untag/<path:path>?project_path=<path:project_path>')
def untag(path, project_path):
    session['logged_in'] = True
    flash("Removed tag '{}'".format(os.path.basename(project_path)))
    _execute_pipe(g.data_path,
                  "untag", ["/" + path, "/" + project_path], {})

    return redirect(url_for('show_node', path=path))
