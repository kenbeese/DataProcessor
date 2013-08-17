# coding=utf-8
import os
import shutil
from glob import glob
from jinja2 import Template


def _strip_invalid_node(node_list):
    result_list = []
    for node in node_list:
        if node["type"] == "run" and "path" in node and "configure" in node:
            result_list.append(node)
        elif node["type"] == "project" and "path" in node:
            result_list.append(node)
    return result_list


def _replace(node, template_html, output_html):
    cfg = {
        "node": node,
        "output_html": output_html
    }
    with open(template_html, 'r') as f:
        tmpl = Template(f.read())
    html = tmpl.render(cfg)
    output_path = os.path.join(node["path"], output_html)
    with open(output_path, 'w') as f:
        f.write(html.encode("utf-8"))
    return node


def _install_attachments(template_dir, dest_path):
    if not os.path.isdir(template_dir):
        print("template directory does not found.")
        return 1
    if not os.path.isdir(dest_path):
        print("destination directory does not found.")
        return 1
    attachments = ["js", "css"]
    for att in attachments:
        path = os.path.join(template_dir, att)
        if not os.path.isdir(path):
            continue
        att_dest_dir = os.path.join(dest_path, att)
        if not os.path.isdir(att_dest_dir):
            os.mkdir(att_dest_dir)
        for a in glob(os.path.join(path, u"*." + att)):
            shutil.copy2(a, att_dest_dir)


def generate(node_list, template_dir, output_html,
             install_attachments=False,
             template_filename={"project": "template_project.html",
                                "run": "template_run.html"}):
    template_dir = os.path.expanduser(template_dir)
    node_list = _strip_invalid_node(node_list)
    for node in node_list:
        if install_attachments:
            _install_attachments(template_dir, node["path"])
        template_path = os.path.join(
            template_dir, template_filename[node["type"]])
        _replace(node, template_path, output_html)
    return node_list


def register(pipes_dics):
    pipes_dics["generate_html"] = {
        "func": generate,
        "args": ["template_path", "output_html"],
        "desc": "generate HTML and install attachments",
        "kwds": ["install_attachments", "template_filename"],
    }
