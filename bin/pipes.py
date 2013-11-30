#!/usr/bin/python

""" Generate a document for pipes """

import os.path
import sys
import copy
from jinja2 import Template

ProjectHome = os.path.join(os.path.dirname(__file__), "..")
sys.path = ([sys.path[0]]
            + [os.path.join(ProjectHome, "lib")]
            + sys.path[1:])
import dataprocessor as dp
sys.path = [sys.path[0]] + sys.path[2:]


def document():
    with open(os.path.join(ProjectHome, "template/pipes.md"), 'r') as f:
        template = Template(f.read())
    pipe_dict = copy.deepcopy(dp.pipes.pipes_dics)
    pipe_list = []
    for pipe_name in pipe_dict:
        d = {"name": pipe_name}
        d.update(pipe_dict[pipe_name])
        pipe_list.append(d)
        pipe_list.sort(key=lambda pipe :  pipe["name"])
    pipe_doc_md = template.render(pipes=pipe_list)
    with open(os.path.join(ProjectHome, "doc/pipes.md"), 'w') as f:
        f.write(pipe_doc_md)


if __name__ == "__main__":
    document()
