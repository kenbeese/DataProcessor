# coding=utf-8
from . import utility

import json
import os.path


def save(node_list, json_path, ask_replace=True):
    """
    save node_list into a JSON file
    """
    path = utility.path_expand(json_path)
    if ask_replace and os.path.exists(path):
        ans = raw_input("File %s already exists. Replace? [y/N]"
                        % json_path).lower()
        if ans not in ["yes", "y"]:
            print("Skip save_json pipe.")
            return node_list
    with open(path, "w") as f:
        json.dump(node_list, f, indent=4)
    return node_list


def load(node_list, json_path):
    """
    load node_list from a JSON file
    """
    path = utility.path_expand(json_path)
    if not os.path.exists(path):
        raise RuntimeError("JSON does not exist")
    with open(path, "r") as f:
        read_node_list = json.load(f)
    return node_list + read_node_list


if __name__ == "__main__":
    import doctest
    doctest.testmod()
