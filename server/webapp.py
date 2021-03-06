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
    with dp.io.SyncDataHandler(g.data_path) as dh:
        nl = dh.get()
    projects = dp.filter.node_type(nl, "project")
    for p in projects:
        p["num_children"] = len(p["children"])
    return render_template('projectlist.html', projects=projects)


@app.route('/runlist')
def show_runlist():
    with dp.io.SyncDataHandler(g.data_path) as dh:
        nl = dh.get()
    runs = dp.filter.node_type(nl, "run")
    for n in runs:
        n["tag-nodes"] = [dp.nodes.get(nl, p) for p in n["parents"]]
    return render_template('runlist.html', runs=runs)


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
    with dp.io.SyncDataHandler(g.data_path) as dh:
        nl = dh.get()

    node = dp.nodes.get(nl, path)

    show_function = {
        "run": show_run,
        "project": show_project,
        "ipynb": show_ipynb,
    }
    return show_function[node["type"]](node, nl)


def show_run(node, node_list):

    # for tag
    parent_nodes = []
    for p in node["parents"]:
        parent_nodes.append(dp.nodes.get(node_list, p))

    # for completion of add tag
    project_id_nodes = dp.filter.prefix_path(node_list, dp.basket.get_project_basket())
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
    ipynb_names = [n["name"] for n in ipynb_nodes]

    # files
    path = node["path"]
    non_seq, seq = dp.utility.detect_sequence(os.listdir(path))
    dirs = sorted([name for name in non_seq if os.path.isdir(os.path.join(path, name))])
    files = sorted([(dp.utility.expect_filetype(name), name)
                    for name in non_seq if name not in dirs and name not in ipynb_names], reverse=True)
    patterns = [(pat, len(seq[pat])) for pat in sorted(seq.keys())]

    return render_template("run.html", node=node, ipynb=ipynb_nodes, files=files, dirs=dirs,
                           sequences=patterns, parents=parent_nodes, project_ids=project_ids)


def show_project(node, node_list):
    # for tag
    parent_nodes = []
    for p in node["parents"]:
        parent_nodes.append(dp.nodes.get(node_list, p))

    # for completion of add tag
    project_id_nodes = dp.filter.prefix_path(node_list, dp.basket.get_project_basket())
    project_ids = [n["name"] for n in project_id_nodes]

    df = dp.dataframe.get_project(node_list, node["path"], properties=["comment"])
    if not df.empty:
        index = sorted(df.columns, reverse=True, key=lambda col: len(set(df[col])))
        cfg = [c for c in index if c not in ["name", "comment"]]
    else:
        cfg = None
    return render_template("project.html", df=df, cfg=cfg, node=node,
                           parents=parent_nodes, project_ids=project_ids)


def show_ipynb(node, node_list):
    parent_nodes = []
    for p in node["parents"]:
        parent_nodes.append(dp.nodes.get(node_list, p))
    project_id_nodes = dp.filter.prefix_path(node_list, dp.basket.get_project_basket())
    project_ids = [n["name"] for n in project_id_nodes]
    nb = dp.ipynb.gather_notebooks()
    try:
        node["url"] = dp.ipynb.resolve_url(node["path"], nb)
    except dp.exception.DataProcessorError:
        node["url"] = ""
    return render_template("ipynb.html", node=node, parents=parent_nodes, project_ids=project_ids)


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
    with dp.io.SyncDataHandler(data_path) as dh:
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


@app.route('/delete_project', methods=['POST'])
def delete_project():
    path = request.form['path']
    session['logged_in'] = True
    _execute_pipe(g.data_path, "remove_node", [path], {})
    return Response()
