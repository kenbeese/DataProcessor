# -*- coding: utf-8 -*-

import os.path as op
from jinja2 import Template

from ..utility import check_directory
from ..filter import node_type
from ..dataframe import get_project
from ..ipynb import resolve_url, resolve_name
from ..exception import DataProcessorError as dpError
from .. import nodes

template_dir = check_directory(op.join(__file__, "../../../../template/"))


def projectlist(node_list):
    with open(op.join(template_dir, "projectlist.html"), "r") as f:
        template = Template(f.read())
    projects = node_type(node_list, "project")
    print(template.render(projects=projects))
    return node_list


def project(node_list, path):
    df = get_project(node_list, path, properties=["comment"]).fillna("")
    with open(op.join(template_dir, "project.html"), "r") as f:
        template = Template(f.read())

    def _count_uniq(col):
        return len(set(df[col]))
    index = sorted(df.columns, key=_count_uniq, reverse=True)
    cfg = [c for c in index if c not in ["name", "comment"]]
    print(template.render(df=df, cfg=cfg))
    return node_list


def run(node_list, path):
    node = nodes.get(node_list, path)
    with open(op.join(template_dir, "run.html"), "r") as f:
        template = Template(f.read())

    ipynb_nodes = []
    for p in node["children"]:
        n = nodes.get(node_list, p).copy()
        if n["type"] != "ipynb":
            continue
        try:
            n["url"] = resolve_url(p)
        except dpError:
            n["url"] = ""
        n["name"] = resolve_name(p)
        ipynb_nodes.append(n)

    print(template.render(node=node, ipynb=ipynb_nodes))
    return node_list


def register(dicts):
    dicts["projectlist_html"] = {
        "func": projectlist,
        "args": [],
        "kwds": [],
        "desc": "output project list in HTML",
        "output": "html",
    }
    dicts["project_html"] = {
        "func": project,
        "args": ["path"],
        "kwds": [],
        "desc": "output project page in HTML",
        "output": "html",
    }
    dicts["run_html"] = {
        "func": run,
        "args": ["path"],
        "kwds": [],
        "desc": "output run page in HTML",
        "output": "html",
    }
