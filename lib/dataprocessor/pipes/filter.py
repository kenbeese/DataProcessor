# coding=utf-8

from .. import filter as flt


def register(pipes_dics):
    pipes_dics["filter_project"] = {
        "func": flt.project,
        "args": ["path"],
        "desc": """filter by project path.
        This pipe filters out runs which don't belong to the project,
        and should be used with '-o' in dpmanip.
        """,
    }
    pipes_dics["filter_node_type"] = {
        "func": flt.node_type,
        "args": ["node_type"],
        "desc": """filter by node type.
        This pipe filters out nodes which has different type attribute,
        and should be used with '-o' option in dpmanip.
        """,
    }
    pipes_dics["filter_prefix"] = {
        "func": flt.prefix_path,
        "args": [("prefix_path",
                  {"help": """Absolute path or relative path.
                   The relative path will be expanded to absolute path."""})],
        "desc": """filter by prefix_path.
        This pipe filters out runs, projects and figures
        whose path does not start with the prefix,
        and should be used with '-o' option in dpmanip.
        """
    }
