# coding=utf-8
import os.path


def add_figure_node(node_list, path, figure_names,
                    parents, children):
    # check
    path = os.path.expanduser(os.path.abspath(path))
    if not os.path.exists(path):
        raise RuntimeError("figure directory does not found")
    for fig_name in figure_names:
        fig_path = os.path.join(path, fig_name)
        if not os.path.exists(fig_path):
            raise RuntimeError("figure %s does not found" % fig_name)

    # create node
    node = {
        "path": path,
        "type": "figure",
        "figures": figure_names,
        "parents": parents,
        "children": children,
    }
    node_list.append(node)
