# coding=utf-8

def _get_confs(run_list):
    confs = []
    for run in run_list:
        conf = run["configure"]
        for c in conf:
            if c not in confs:
                confs.append(c)
    confs.sort()
    confs.sort(key=len)
    return confs

def _strip_invalid_run(run_list):
    result_list = []
    for run in run_list:
        if "path" in run and "meta" in run and "configure" in run:
            result_list.append(run)
    return result_list

from jinja2 import Template
def replace(run_list,template_filename,output_filename,pre_meta,post_meta,confs):
    stripped_list = _strip_invalid_run(run_list)
    if not confs:
        confs = _get_confs(stripped_list)
    cfg = { "run_list" : stripped_list,
            "confs" : confs,
            "pre_meta" : pre_meta,
            "post_meta" : post_meta,
        }
    with open(template_filename,'r') as f:
        tmpl = Template(f.read())
    html = tmpl.render(cfg)
    with open(output_filename,'w') as f:
        f.write(html.encode("utf-8"))
    return run_list

import os
import os.path
import shutil
from glob import glob
def _install_attachments(template_dir,dest_path):
    if not os.path.isdir(template_dir):
        print("template directory does not found.")
        return 1
    if not os.path.isdir(dest_path):
        print("destination directory does not found.")
        return 1
    attachments = ["js","css"]
    for att in attachments:
        path = os.path.join(template_dir,att)
        if not os.path.isdir(path):
            continue
        att_dest_dir = os.path.join(dest_path,att)
        if not os.path.isdir(att_dest_dir):
            os.mkdir(att_dest_dir)
        for a in glob(os.path.join(path,u"*."+att)):
            shutil.copy2(a,att_dest_dir)

def generate(run_list,template_dir,output_html_path,template_html_filename="template.html",install_attachments=False,pre_meta=["name","date"],post_meta=["tags","comment"],confs=None):
    output_html_path = os.path.expanduser(output_html_path)
    dest_dir = os.path.dirname(output_html_path)
    if install_attachments:
        _install_attachments(template_dir,dest_dir)
    template_html_path = os.path.join(template_dir,template_html_filename)
    replace(run_list,template_html_path,output_html_path,pre_meta,post_meta,confs)

def register(pipes_dics):
    pipes_dics["generate_html"] = {
        "func" : generate,
        "args" : ["template_dir","output_html_path"],
        "desc" : "generate HTML and install attachments",
        "kwds" : ["template_html_filename","install_attachments","pre_meta","post_meta","confs"],
        }
