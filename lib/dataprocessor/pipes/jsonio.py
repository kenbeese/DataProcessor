# coding=utf-8
import json
import os.path


def save(node_list, json_path):
    # TODO check file in json_path already exists
    path = os.path.expanduser(json_path)
    with open(path, "w") as f:
        json.dump(node_list, f)
    return node_list


def load(node_list, json_path):
    if not os.path.exists(json_path):
        raise RuntimeError("json path does not exist")
    path = os.path.expanduser(json_path)
    with open(path, "r") as f:
        read_node_list = json.load(f)
    return node_list + read_node_list


def _test():
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    _test()
