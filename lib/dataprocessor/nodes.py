# coding=utf-8
from .exception import DataProcessorError


def get(node_list, path):
    """search node from node_list by its path

    Returns
    -------
    node or None
        the node is returned if exists,
        and `None` is returned if not.

    Examples
    --------
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


def add(node_list, node, skip_validate_link=False):
    """Add a node into node_list

    This adds a node into node_list,
    and validate links in node["children"] and node["parents"]

    Parameters
    ----------
    node_list : list
        the list of nodes
    node : dict
        The node will be added into node_list
    skip_validate_link : bool, optional
        skip link validation (default False)
    """
    node_list.append(node)
    if not skip_validate_link:
        validate_link(node_list, node)


def remove(node_list, path, skip_validate_link=False):
    """Remove node from node_list

    Parameters
    ----------
    node_list : list
        the list of nodes
    path : str
        The path of the node to be removed
    skip_validate_link : bool, optional
        skip link validation (default False)

    Raises
    ------
    DataProcessorError
        occurs when specified `path` does not exist in node_list

    Examples
    --------
    >>> import copy
    >>> node_list_base = [{
    ...     "path": "/path/0",
    ...     "parents": ["/path/1"],
    ...     "children": ["/path/2", "/path/3"],
    ... },{
    ...     "path": "/path/1",
    ...     "parents": [],
    ...     "children": ["/path/0"],
    ... },{
    ...     "path": "/path/2",
    ...     "parents": ["/path/0"],
    ...     "children": [],
    ... },{
    ...     "path": "/path/3",
    ...     "parents": ["/path/0"],
    ...     "children": [],
    ... }]
    >>> node_list = copy.deepcopy(node_list_base)
    >>> remove(node_list, "/path/0")
    >>> node_list == [{
    ...     'path': '/path/1',
    ...     'parents': [],
    ...     'children': []
    ... }, {
    ...     'path': '/path/2',
    ...     'parents': [],
    ...     'children': []
    ... }, {
    ...     'path': '/path/3',
    ...     'parents': [],
    ...     'children': []
    ... }]
    True
    >>> node_list = copy.deepcopy(node_list_base)
    >>> remove(node_list, "/path/1")
    >>> node_list == [{
    ...     'path': '/path/0',
    ...     'parents': [],
    ...     'children': ['/path/2', '/path/3']
    ... }, {
    ...     'path': '/path/2',
    ...     'parents': ['/path/0'],
    ...     'children': []
    ... }, {
    ...     'path': '/path/3',
    ...     'parents': ['/path/0'],
    ...     'children': []
    ... }]
    True
    >>> node_list = copy.deepcopy(node_list_base)
    >>> remove(node_list, "/path/3")
    >>> node_list == [{
    ...     'path': '/path/0',
    ...     'parents': ['/path/1'],
    ...     'children': ['/path/2']
    ... }, {
    ...     'path': '/path/1',
    ...     'parents': [],
    ...     'children': ['/path/0']
    ... }, {
    ...     'path': '/path/2',
    ...     'parents': ['/path/0'],
    ...     'children': []
    ... }]
    True
    """
    node = get(node_list, path)
    if not node:
        raise DataProcessorError("Removing non-existing node.")
    if not skip_validate_link:
        path = node["path"]
        for p_path in node["parents"]:
            p_node = get(node_list, p_path)
            if not p_node:
                continue
            p_node["children"].remove(path)
        for c_path in node["children"]:
            c_node = get(node_list, c_path)
            if not c_node:
                continue
            c_node["parents"].remove(path)
    node_list.remove(node)


def validate_link(node_list, node, silent=False):
    """validate the link of the node

    Check node["children"] and node["parents"] is correct.
    If a link is incomplete, it will fixed (see the following example).

    Parameters
    ----------
    node_list : list
        the list of nodes
    node : dict
        a node will be checked.
        This must belong to the `node_list`

    Examples
    --------
    >>> node_list = [{
    ...     "path": "/path/0",
    ...     "parents": ["/path/1"],
    ...     "children": ["/path/2", "/path/3"],
    ... },{
    ...     "path": "/path/1",
    ...     "parents": [],
    ...     "children": ["/path/0"],
    ... },{
    ...     "path": "/path/2",
    ...     "parents": [], # incomplete
    ...     "children": [],
    ... },{
    ...     "path": "/path/3",
    ...     "parents": ["/path/0"],
    ...     "children": ["/path/4"], # does not exist
    ... }]
    >>> validate_link(node_list, node_list[0])
    >>> node_list == [{
    ...     "path": "/path/0",
    ...     "parents": ["/path/1"],
    ...     "children": ["/path/2", "/path/3"],
    ... },{
    ...     "path": "/path/1",
    ...     "parents": [],
    ...     "children": ["/path/0"],
    ... },{
    ...     "path": "/path/2",
    ...     "parents": ["/path/0"], # refined
    ...     "children": [],
    ... },{
    ...     "path": "/path/3",
    ...     "parents": ["/path/0"],
    ...     "children": ["/path/4"], # This error is kept
    ... }]
    True
    >>> validate_link(node_list, node_list[3], silent=True)
    >>> node_list == [{
    ...     "path": "/path/0",
    ...     "parents": ["/path/1"],
    ...     "children": ["/path/2", "/path/3"],
    ... },{
    ...     "path": "/path/1",
    ...     "parents": [],
    ...     "children": ["/path/0"],
    ... },{
    ...     "path": "/path/2",
    ...     "parents": ["/path/0"],
    ...     "children": [],
    ... },{
    ...     "path": "/path/3",
    ...     "parents": ["/path/0"],
    ...     "children": [], # removed
    ... }]
    True
    """
    path = node["path"]

    def ask_remove(path):
        print("No nodes whose path is %s does not exists." % path)
        ans = raw_input("Remove this link? [Y/n]")
        if ans in ["n", "N", "no", "No"]:
            print("Path %s is kept. Please fix manually." % path)
            return False
        else:
            print("Removed.")
            return True

    def validate(check_key):
        against_key = {"parents": "children", "children": "parents"}[check_key]
        link_path_list = []
        for link_path in node[check_key]:
            link_node = get(node_list, link_path)
            if link_node:
                link_path_list.append(link_path)
                if path not in link_node[against_key]:
                    link_node[against_key].append(path)
            else:
                if silent:
                    continue
                if ask_remove(path):
                    link_path_list.append(link_path)
        node[check_key] = link_path_list

    validate("parents")
    validate("children")
