# coding=utf-8
from .exception import DataProcessorError
from . import utility

import json
import os.path


def save(node_list, json_path, silent=False):
    """save node_list into a JSON file

    Parameters
    ----------
    json_path: str
        the path to JSON
    slient: bool, str, optional
        Ask whether replace JSON file (default=False)
    """
    silent = utility.boolenize(silent)
    path = utility.path_expand(json_path)
    if not silent and os.path.exists(path):
        ans = raw_input("File %s already exists. Replace? [y/N]"
                        % json_path).lower()
        if ans not in ["yes", "y"]:
            print("Skip save_json pipe.")
            return node_list
    with open(path, "w") as f:
        json.dump(node_list, f, indent=4)
    return node_list


def load(node_list, json_path):
    """load node_list from a JSON file

    Parameters
    ----------
    json_path: str
        the path to JSON

    Returns
    -------
    list
        node_list(arg1) + [new node list]

    Raises
    ------
    DataProcessorError
        occurs when JSON file does not exist.
    """
    path = utility.path_expand(json_path)
    if not os.path.exists(path):
        raise DataProcessorError("JSON does not exist")
    with open(path, "r") as f:
        read_node_list = json.load(f)
    return node_list + read_node_list
