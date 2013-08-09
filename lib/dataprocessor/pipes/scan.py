import os
from glob import glob


def directory(node_list, root, whitelist):
    root = os.path.abspath(os.path.expanduser(root))
    for path, dirs, files in os.walk(root):
        node_type = None
        parents = []
        children = []
        for child in dirs:
            for white in whitelist:
                if glob(os.path.join(path, child, white)):
                    node_type = "project"
                    children.append(os.path.join(path, child))
                    break
        for white in whitelist:
            if glob(os.path.join(path, white)):
                node_type = "run"
                parents.append(os.path.dirname(path))
                break
        if not node_type:
            continue
        node_list.append({"path": path,
                          "parents": parents,
                          "children": children,
                          "type": node_type,
                          "name": os.path.basename(path),
                          })
    return node_list


def register(pipe_dics):
    pipe_dics["scan_directory"] = {
        "func": directory,
        "args": ["root_path", "whitelist"],
        "desc": "scan direcoty structure",
    }


if __name__ == "__main__":
    node_list = directory([], "~/data", ["*.conf"])
    print(node_list)
