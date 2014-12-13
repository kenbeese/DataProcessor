# coding: utf-8

from .. import nodes


def remove_node(node_list, path):
    nodes.remove(node_list, path, skip_validate_link=False)


def register(pipes_dics):
    pipes_dics["remove_node"] = {
        "func": remove_node,
        "args": ["path"],
        "desc": """Remove the information of run or project from the database of this tool.
        Dose not remove the directory of run or project.""",
    }
