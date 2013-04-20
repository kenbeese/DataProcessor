# coding=utf-8

def meta_filter(run_list,key,value):
    result_list = []
    for run in run_list:
        if key in run["meta"] and run["meta"][key] == value:
            result_list.append(run)
    return result_list

def register(filter_list):
    filter_list["meta_filter"] = {
        "func" : meta_filter,
        "args" : ["key","value"],
        "desc" : "leave runs whose 'project' is project_name",
        }

