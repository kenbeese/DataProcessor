# coding=utf-8
import os.path


def _check_files(path, figure_names):
    """
    check if figures exist in path
    """
    if not os.path.exists(path):
        raise RuntimeError("figure directory does not found")
    for fig_name in figure_names:
        fig_path = os.path.join(path, fig_name)
        if not os.path.exists(fig_path):
            raise RuntimeError("figure %s does not found" % fig_name)


def add_figure_node(node_list, path, figure_names,
                    parents, children, check_files=True):
    """
    add figure node into node_list

    It is assumed that figures have been generated already
    by another way. This function only generate a node.

    >>> node_list = []
    >>> node_list = add_figure_node(
    ...                 node_list,"/tmp/doctest/add_figure_node/fig1",
    ...                 ["fig1.eps","fig1.png"],
    ...                 ["/tmp/doctest/add_figure_node"],
    ...                 ["/path/to/run/data"],
    ...                 check_files=False
    ...             )
    >>> node_list == [{'path': '/tmp/doctest/add_figure_node/fig1',
    ...                'type': 'figure',
    ...                'figures': ['fig1.eps', 'fig1.png'],
    ...                'parents': ['/tmp/doctest/add_figure_node'],
    ...                'children': ['/path/to/run/data']}]
    True
    """
    path = os.path.expanduser(os.path.abspath(path))
    if check_files:
        _check_files(path, figure_names)
    node = {
        "path": path,
        "type": "figure",
        "figures": figure_names,
        "parents": parents,
        "children": children,
    }
    node_list.append(node)
    return node_list


def register(pipe_dics):
    pipe_dics["add_figure_node"] = {
        "func": add_figure_node,
        "args": ["path", "figure_names", "parents", "children"],
        "desc": "add figure node into node_list",
    }


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
