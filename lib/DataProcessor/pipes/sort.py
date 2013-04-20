# coding=utf-8

import re
def sort_name(run_list):
    def _strip_int(run):
        name = run["meta"]["name"]
        return int(re.search(r'[0-9]+',name).group())
    run_list.sort(key=_strip_int)
    return run_list

def register(filter_list):
    filter_list["sort_name"] = {
        "func" : sort_name,
        "args" : [],
        "desc" : "sort name",
        }


