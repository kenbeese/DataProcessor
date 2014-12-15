# -*- coding: utf-8 -*-

import os.path as op
from jinja2 import Template

from ..utility import check_directory
from ..filter import node_type

template_dir = check_directory(op.join(__file__, "../../../../template/"))


def project_table(node_list):
    with open(op.join(template_dir, "project_table.html"), "r") as f:
        template = Template(f.read())
    projects = node_type(node_list, "project")
    print(template.render(projects=projects))
    return node_list


def register(dicts):
    dicts["project_table"] = {
        "func": project_table,
        "args": [],
        "kwds": [],
        "desc": "output project HTML table",
        "output": "html",
    }
