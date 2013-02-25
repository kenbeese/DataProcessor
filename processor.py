# coding=utf-8

from . import input_dic,output_dic
from .filters import filter_dic

def processing(action_list):
    in_dic = input_dic[action_list["input"]["name"]]
    run_list = in_dic["func"](in_dic["args"])

    for f in action_list["filter"]:
        f_dic = filter_dic[f["name"]]
        run_list = f_dic["func"](run_list,f_dic["args"])

    out_dic = output_dic[action_list["output"]["name"]]
    out_dic["func"](run_list,out_dic["args"])

def test():
    action_list_sample = {
            "input"  : {"name":"sample","args":[]},
            "output" : {"name":"csv","args":[]},
            "filter" : [
                    {"name":"meta","args":[]},
                    {"name":"project_choose","args":["P1"]}
               ],
        }
    processing(action_list_sample)

