# coding=utf-8

import os.path
def meta(run_list,args):
    for run in run_list:
        path = run["path"]
        name = os.path.basename(path)
        project = os.path.basename(os.path.dirname(path))
        run["meta"] = {
                "name"    : name,
                "project" : project,
            }
    return run_list

def register(filter_list):
    filter_list["meta"] = {
        "func" : meta,
        "args" : [],
        "desc" : "add meta data",
        }

