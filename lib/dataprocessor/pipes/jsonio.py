# coding=utf-8
from .. import io


def register(pipes_dics):
    pipes_dics["save_json"] = {
        "func": io.save,
        "args": ["json_path"],
        "kwds": [],
        "desc": "save node_list in a JSON file",
    }
    pipes_dics["load_json"] = {
        "func": io.load,
        "args": ["json_path"],
        "desc": "load node_list from a JSON file",
    }
