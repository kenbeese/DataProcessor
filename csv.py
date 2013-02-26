# coding=utf-8

def csv(run_list,args):
    filename = args[0]
    f = open(filename,"w")
    for run in run_list:
        path = run["path"]
        f.write(path+'\n')

def register(filter_list):
    filter_list["csv"] = {
        "func" : csv,
        "args" : ["filename"],
        "desc" : "output to csv file",
        }

