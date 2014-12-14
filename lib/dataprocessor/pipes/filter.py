# coding=utf-8

from .. import filter as flt


def register(pipes_dics):
    pipes_dics["filter_project"] = {
        "func": flt.project,
        "args": ["path"],
        "desc": """filter by project path.
        This pipe reduce database. In `dpmanip`, std output option '-o' should be used.
        """,
    }
    pipes_dics["filter_node_type"] = {
        "func": flt.node_type,
        "args": ["node_type"],
        "desc": """filter by node type.
        This pipe reduce database. In `dpmanip`, std output option '-o' should be used.
        """,
    }
    pipes_dics["filter_path"] = {
        "func": flt.prefix_path,
        "args": ["pre_path"],
        "desc": """filter by prefix_path.
        This pipe reduce database. In `dpmanip`, std output option '-o' should be used.
        """
    }
