# coding=utf-8
import os

from jinja2 import Template


def _strip_invalid_node(node_list):
    result_list = []
    for node in node_list:
        if node["type"] == "run" and "path" in node and "configure" in node:
            result_list.append(node)
        elif node["type"] == "project" and "path" in node:
            result_list.append(node)
    return result_list


def _get_widget_html(widget, output_html, template_dir):
    widget_html = {"type": widget["type"]}
    html_filename = os.path.join(template_dir,
                                 "widget_" + widget["type"] + ".html")
    with open(html_filename, 'r') as f:
        tmpl = Template(f.read())
    widget_html["html"] = tmpl.render(widget, output_html=output_html)
    return widget_html


def _replace(node, template_html, output_html):
    cfg = {
        "node": node,
        "widgets": [],
    }
    if "widgets" in node:
        for widget in node["widgets"]:
            cfg["widgets"].append(
                _get_widget_html(widget, output_html,
                                 os.path.dirname(template_html)))
    with open(template_html, 'r') as f:
        tmpl = Template(f.read())
    html = tmpl.render(cfg)
    output_path = os.path.join(node["path"], output_html)
    with open(output_path, 'w') as f:
        f.write(html.encode("utf-8"))
    return node


def generate(node_list, template_dir, output_html,
             template_filename={"project": "template_project.html",
                                "run": "template_run.html"}):
    """
    Convert each node to html. No node_list changes at all.

    Notes:
    Output files are created at relative path of each node as same name.
    Run node must have key 'configure'.
    """
    template_dir = os.path.expanduser(template_dir)
    node_list = _strip_invalid_node(node_list)
    for node in node_list:
        template_path = os.path.join(
            template_dir, template_filename[node["type"]])
        _replace(node, template_path, output_html)
    return node_list


def register(pipes_dics):
    pipes_dics["generate_html"] = {
        "func": generate,
        "args": ["template_path", "output_html"],
        "desc": "generate HTML and install attachments",
        "kwds": ["template_filename"],
    }
