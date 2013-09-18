# coding=utf-8


def get(node_list, path):
    """
    search node from node_list by its path

    >>> node_list = [{"path": "/path/1"}, {"path": "/path/2"},
    ...              {"path": "/path/3"}, {"path": "/path/4"}]
    >>> get(node_list, "/path/3")
    {'path': '/path/3'}
    >>> node = get(node_list, "/path/5") # no node exists
    >>> print(node)
    None
    """
    for node in node_list:
        if path == node["path"]:
            return node
    return None


def add(node_list, node, no_validate_link=False):
    """
    Add node into node_list,
    and check node["children"] and node["parent"]

    If flag "no_validate_link" is specified,
    the check will be skipped.
    """
    node_list.append(node)
    if not no_validate_link:
        validate_link(node_list, node)


def _ask_remove(path):
    print("No nodes whose path is %s does not exists.")
    ans = raw_input("Remove this link? [Y/n]")
    if ans in ["n", "N", "no", "No"]:
        print("Path %s is kept. Please fix manually." % path)
        return False
    else:
        print("Removed.")
        return True


def validate_link(node_list, node, ask_remove=True):
    """
    validate the link of the node

    >>> node_list = [{
    ...     "path": "/path/1",
    ...     "parents": ["/path/2"],
    ...     "children": ["/path/3", "/path/4"],
    ... },{
    ...     "path": "/path/2",
    ...     "parents": [],
    ...     "children": ["/path/1"],
    ... },{
    ...     "path": "/path/3",
    ...     "parents": [], # incomplete
    ...     "children": [],
    ... },{
    ...     "path": "/path/4",
    ...     "parents": ["/path/1"],
    ...     "children": ["/path/5"], # does not exist
    ... }]
    >>> validate_link(node_list, node_list[0])
    >>> node_list == [{
    ...     "path": "/path/1",
    ...     "parents": ["/path/2"],
    ...     "children": ["/path/3", "/path/4"],
    ... },{
    ...     "path": "/path/2",
    ...     "parents": [],
    ...     "children": ["/path/1"],
    ... },{
    ...     "path": "/path/3",
    ...     "parents": ["/path/1"], # refined
    ...     "children": [],
    ... },{
    ...     "path": "/path/4",
    ...     "parents": ["/path/1"],
    ...     "children": ["/path/5"], # This error is kept
    ... }]
    True
    >>> validate_link(node_list, node_list[3], ask_remove=False)
    >>> node_list == [{
    ...     "path": "/path/1",
    ...     "parents": ["/path/2"],
    ...     "children": ["/path/3", "/path/4"],
    ... },{
    ...     "path": "/path/2",
    ...     "parents": [],
    ...     "children": ["/path/1"],
    ... },{
    ...     "path": "/path/3",
    ...     "parents": ["/path/1"],
    ...     "children": [],
    ... },{
    ...     "path": "/path/4",
    ...     "parents": ["/path/1"],
    ...     "children": [], # removed
    ... }]
    True
    """
    path = node["path"]

    # for parents
    remove_path_list = []
    for parent_path in node["parents"]:
        p_node = get(node_list, parent_path)
        if not p_node:
            if not ask_remove or _ask_remove(parent_path):
                remove_path_list.append(parent_path)
            continue
        if path not in p_node["children"]:
            p_node["children"].append(path)
    for path in remove_path_list:
        node["parents"].remove(path)

    # for children
    remove_path_list = []
    for child_path in node["children"]:
        c_node = get(node_list, child_path)
        if not c_node:
            if not ask_remove or _ask_remove(child_path):
                remove_path_list.append(child_path)
            continue
        if path not in c_node["parents"]:
            c_node["parents"].append(path)
    for path in remove_path_list:
        node["children"].remove(path)


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
