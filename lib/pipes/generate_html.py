# coding=utf-8

from jinja2 import Template
def replace(run_list,template_filename,output_filename):
    result_list = []
    confs = []
    for run in run_list:
        if "path" not in run or "meta" not in run or "configure" not in run:
            continue
        conf = run["configure"]
        for c in conf:
            if c not in confs:
                confs.append(c)
        result_list.append(run)
    confs.sort()
    confs.sort(key=len)
    cfg = { "run_list" : result_list,
            "confs" : confs,
            "pre_meta" : ["name","date"],
            "post_meta" : ["tags","comment"]
        }
    with open(template_filename,'r') as f:
        tmpl = Template(f.read())
    html = tmpl.render(cfg)
    with open(output_filename,'w') as f:
        f.write(html.encode("utf-8"))
    return run_list

import os.path
import shutil
def _install_attachments(template_dir,dest_path):
    if not os.path.isdir(template_dir):
        print("template directory does not found.")
        return 1
    if not os,path.isdir(dest_path):
        print("destination directory does not found.")
        return 1
    attachments = ["js","css"]
    att_paths = [os.path.join(template_dir,att) for att in attachments]
    att_paths = [path for path in att_paths if os.path.exists(path)]
    for att_path in att_paths:
        shutil.copytree(att_path,dest_path)

def generate(run_list,template_dir,output_html_path,template_html_filename="template.html",install_attachment=False):
    output_html_path = os.path.abspath(output_html_path)
    dest_dir = os.path.dirname(output_html_path)
    if install_attachment:
        _install_attachments(template_dir,dest_dir)
    template_html_path = os.path(template_dir,template_html_filename)
    replace(run_list,template_html_path,output_html_path)

def register(pipes_dics):
    pipes_dics["generate_html"] = {
        "func" : replace,
        "args" : ["template_dir","output_html_path"],
        "desc" : "generate HTML and install attachments",
        "kwds" : ["template_html_filename","install_attachments"],
        }
