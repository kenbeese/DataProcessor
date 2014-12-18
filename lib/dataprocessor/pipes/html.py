# -*- coding: utf-8 -*-

import json
import os.path as op
from jinja2 import Template

from ..utility import check_directory
from ..filter import node_type
from ..dataframe import get_project
from .. import nodes

template_dir = check_directory(op.join(__file__, "../../../../template/"))


def projectlist(node_list):
    with open(op.join(template_dir, "projectlist.html"), "r") as f:
        template = Template(f.read())
    projects = node_type(node_list, "project")
    res = {
        "paths": [node["path"] for node in projects],
        "html": template.render(projects=projects),
    }
    print(json.dumps(res))
    return node_list


def project(node_list, path):
    node = nodes.get(node_list, path)
    df = get_project(node_list, path, properties=["comment"])
    res = {
        "name": node["name"],
        # TODO replace with original HTML template
        "html": df.to_html(classes=["table", "table-striped"]), 
    }
    print(json.dumps(res))
    return node_list


def register(dicts):
    dicts["projectlist_html"] = {
        "func": projectlist,
        "args": [],
        "kwds": [],
        "desc": "output project HTML table",
        "output": "json",
    }
    dicts["project_html"] = {
        "func": project,
        "args": ["path"],
        "kwds": [],
        "desc": "output HTML table",
        "output": "json",
    }
