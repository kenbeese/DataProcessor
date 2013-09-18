# coding=utf-8


def get(node_list, path):
    for node in node_list:
        if path == node["path"]:
            return node
