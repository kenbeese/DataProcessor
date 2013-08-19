# coding=utf-8
import json
import os.path


def save(node_list, json_path, ask_replace=True):
    """
    save node_list into a JSON file
    """
    path = os.path.expanduser(json_path)
    if ask_replace and os.path.exists(json_path):
        ans = raw_input("File %s already exists. Replace? [y/N]"
                        % json_path).lower()
        if ans not in ["yes", "y"]:
            print("Skip save_json pipe.")
            return node_list
    with open(path, "w") as f:
        json.dump(node_list, f)
    return node_list


def load(node_list, json_path):
    """
    load node_list from a JSON file
    """
    path = os.path.expanduser(json_path)
    if not os.path.exists(json_path):
        raise RuntimeError("json path does not exist")
    with open(path, "r") as f:
        read_node_list = json.load(f)
    return node_list + read_node_list


def register(pipes_dics):
    pipes_dics["save_json"] = {
        "func": save,
        "args": ["json_path"],
        "kwds": ["ask_replace"],
        "desc": "save node_list in a JSON file",
    }
    pipes_dics["load_json"] = {
        "func": load,
        "args": ["json_path"],
        "desc": "load node_list from a JSON file",
    }


def _test():
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    _test()
