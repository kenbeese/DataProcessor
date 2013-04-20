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

def register(pipes_dics):
    pipes_dics["generate_html"] = {
        "func" : replace,
        "args" : ["template_filename","output_filename"],
        "desc" : "replace jinja2 template",
        }

