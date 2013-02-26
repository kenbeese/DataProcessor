# coding=utf-8

def project_choose(run_list,args):
    result_list = []
    project_name = args[0]
    for run in run_list:
        if "project" not in run["meta"]:
            continue
        if project_name == run["meta"]["project"]:
            result_list.append(run)
    return result_list

def register(filter_list):
    filter_list["project_choose"] = {
        "func" : project_choose,
        "args" : ["project_name"],
        "desc" : "leave runs whose 'project' is project_name",
        }

