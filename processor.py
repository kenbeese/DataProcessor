# coding=utf-8

from . import input_dics,output_dics
from .filters import filter_dics

class ArgsMismatch(Exception):
    def __init__(self,action):
        self.action = action
    def __str__(self):
        return "Name:"+self.action["name"]+" Args:"+(",".join(self.action["args"]))

def get_dic(action,dics):
    dic = dics[action["name"]]
    if len(dic["args"]) != len(action["args"]):
        raise ArgsMismatch(action)
    return dic

def processing(action_list):
    in_action = action_list["input"]
    in_dic = get_dic(in_action,input_dics)
    run_list = in_dic["func"](in_action["args"])

    for f in action_list["filter"]:
        f_dic = get_dic(f,filter_dics)
        run_list = f_dic["func"](run_list,f["args"])

    out_action = action_list["output"]
    out_dic = get_dic(out_action,output_dics)
    out_dic["func"](run_list,out_action["args"])

def test():
    action_list_sample = {
            "input"  : {"name":"sample","args":[]},
            "output" : {"name":"csv","args":["test.csv"]},
            "filter" : [
                    {"name":"meta","args":[]},
                    {"name":"project_choose","args":["P1"]}
               ],
        }
    processing(action_list_sample)

