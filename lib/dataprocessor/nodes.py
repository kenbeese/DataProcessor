# coding=utf-8
"""Tools for manipulation of node_list."""
from .exception import DataProcessorError
from . import utility

node_types = ["run", "project", "figure", "ipynb"]


class DataProcessorNodesError(DataProcessorError):

    """Exception about Nodes processings."""

    def __init__(self, msg):
        DataProcessorError.__init__(self, msg)


def normalize(node):
    """ Normalize node (i.e. fill necessary field).

    Parameters
    ----------
    node: dict
        node that you want to normalize

    Returns
    -------
    dict
        normalized node

    Examples
    --------
    >>> node = {
    ...     "path": "/path/0",
    ...     "type": "run",
    ...     "unknown": ["homhom"]
    ... }
    >>> node = normalize(node)
    >>> node == {
    ...     "path": "/path/0",
    ...     "type": "run",
    ...     "name": "",
    ...     "configure": {},
    ...     "comment": "",
    ...     "parents": [],
    ...     "children": [],
    ...     "unknown": ["homhom"]
    ... }
    True

    """
    if "path" not in node or "type" not in node:
        raise DataProcessorError(
            "cannot normalize: Path and type must be needed")
    new_node = {
        "path": node["path"],
        "type": node["type"],
        "name": "",
        "comment": "",
        "parents": [],
        "children": [],
    }
    if node["type"] == "run":
        new_node["configure"] = {}
    new_node.update(node)
    return new_node


def get(node_list, path):
    """Search node from node_list by its path.

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
    path = utility.abspath(path)
    for node in node_list:
        if path == node["path"]:
            return node
    return None


def modest_update(node_list, node, skip_validate_link=False):
    """ Update node properties modestly

    This keeps values as possible,
    besides the "update" strategy of `add(...)` simply uses `dict.update()`.
    If `node` in the arguments has empty value
    e.g. `node = {"path": "/path/0", "comment" : ""}`,
    this function does not overwrite existing comment of
    the node in `node_list`.

    Parameters
    ----------
    node_list : list
        the list of nodes
    node : dict
        The node will be added into node_list
    skip_validate_link : bool, optional
        skip link validation (default False)

    Raises
    ------
    DataProcessorNodesError
        there is no node whose "path" is `node["path"]`

    Examples
    --------
    >>> node_list = [{
    ...   "path": "/path/0",
    ...   "comment": "some comment",
    ...   "children": [],
    ...   "parents": [],
    ... }]
    >>> node = {
    ...   "path":"/path/0",
    ...   "configure": {"A": 1.0},
    ...   "comment": "",
    ... }
    >>> modest_update(node_list, node)
    >>> node_list == [{
    ...   'comment': 'some comment',
    ...   'path': '/path/0',
    ...   'parents': [],
    ...   'children': [],
    ...   'configure': {'A': 1.0}
    ... }]
    True
    """
    node0 = get(node_list, node["path"])
    if not node0:
        raise DataProcessorNodesError("There is no node [path={}]".format(
                                      node["path"]))
    for key, val in node.items():
        if val:
            node0[key] = val
    if not skip_validate_link:
        validate_link(node_list, node0)


def add(node_list, node, skip_validate_link=False, strategy="raise"):
    """Add a node into node_list.

    This adds a node into node_list,
    and validate links in node["children"] and node["parents"].
    In detail of validate link, see `validate_link`.

    Parameters
    ----------
    node_list : list
        the list of nodes
    node : dict
        The node will be added into node_list
    skip_validate_link : bool, optional
        skip link validation (default False)
    strategy : str, optional {"raise", "update", "modest_update", "replace"}
        The strategy for the case
        where there exists a node whose "path" is same as new one

        - "raise" : raise DataProcessorNodesError (default)
        - "update" : use dict.update to update existing node
        - "modest_update" : use nodes.modest_update to update existing node
        - "replace" : replace existing node with new node

    Raises
    ------
    DataProcessorNodesError:
        there is already exist node whose path is `node["path"]`
    DataProcessorError:
        strategy is invalid string

    Examples
    --------
    >>> node_list = [{"path": "/some/path", "children": [], "parents": []}]
    >>> added_node = {"path": "/added/path", "children": ["/some/path"],
    ...               "parents": []}
    >>> add(node_list, added_node)

    If skip_validate_link=True, snode_list[0]["parents"] is not filled.

    """
    node0 = get(node_list, node["path"])
    if not node0:
        node_list.append(node)
    else:
        if strategy is "raise":
            raise DataProcessorNodesError("node already exists")
        elif strategy is "update":
            node0.update(node)
            node = node0
        elif strategy is "modest_update":
            modest_update(node_list, node,
                          skip_validate_link=skip_validate_link)
            skip_validate_link = False
        elif strategy is "replace":
            node_list.remove(node0)
            node_list.append(node)
        else:
            raise DataProcessorError("Invalid strategy: %s" % strategy)
    if not skip_validate_link:
        validate_link(node_list, node)


def check_duplicate(node_list):
    """ Check if duplicated nodes exist.

    only check their paths

    Parameters
    ----------
    node_list : list
        the list of nodes (not modified)

    Returns
    -------
    list of str
        return the list of duplicated nodes' paths

    Examples
    --------
    >>> node_list = [
    ...     {"path": "/path/0", "parents": ["/path/1"],
    ...      "children": ["/path/2", "/path/3"]},
    ...     {"path": "/path/1", "parents": [],
    ...      "children": ["/path/0"]},
    ...     {"path": "/path/2", "parents": ["/path/0"],
    ...      "children": []},
    ...     {"path": "/path/2", "parents": ["/path/0"],
    ...      "children": []},  # duplicated
    ...     {"path": "/path/3", "parents": ["/path/0"],
    ...      "children": [], "attr1": "value1"},
    ...     {"path": "/path/3", "parents": ["/path/0"],
    ...      "children": [], "attr1": "value2"}  # duplicated
    ... ]
    >>> check_duplicate(node_list)
    ['/path/2', '/path/3']

    """
    paths = []
    dup_paths = []
    for node in node_list:
        path = node["path"]
        if path not in paths:
            paths.append(path)
        else:
            dup_paths.append(path)
    return dup_paths


def merge_duplicate(node_list):
    """ Merge duplicate node.

    If duplicated nodes are found, they will be merged.
    The latter node has priority in merging (see Examples)

    Parameters
    ----------
    node_list : list
        the list of nodes

    Returns
    -------
    node_list : list

    Examples
    --------
    >>> node_list = [
    ...     {"path": "/path/1", "attr1": "value1"},
    ...     {"path": "/path/1", "attr1": "value2"},
    ... ]
    >>> merge_duplicate(node_list)
    [{'path': '/path/1', 'attr1': 'value2'}]

    """
    new_node_list = []
    for node in node_list:
        node0 = get(new_node_list, node["path"])
        if not node0:
            new_node_list.append(node)
            continue
        node0.update(node)
    return new_node_list


def remove(node_list, path, skip_validate_link=False):
    """Remove node from node_list.

    In detail of validate link, see `validate_link`.

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
    >>> node_list = [{"path": "/remove/path", "children": [],
    ...               "parents": ["/some/path"]},
    ...              {"path": "/some/path", "children": ["/remove/path"],
    ...               "parents": []}]
    >>> remove(node_list, "/remove/path")
    >>> node_list
    [{'path': '/some/path', 'parents': [], 'children': []}]

    If skip_validate_link=True, node_list[1]["chilrdren"] is not removed.

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


def validate_link(node_list, node):
    """Validate the link of the node.

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
    Fill node_list[0]'s parents and node_list[1]'s children

    >>> node_list = [
    ...     {"path": "/path/0", "parents": [], "children": []},
    ...     {"path": "/path/1", "parents": [], "children": []},
    ...     {"path": "/path/2", "parents": ["/path/1"],
    ...      "children": ["/path/0"]}]
    >>> validate_link(node_list, node_list[2])
    >>> node_list == [
    ...     {"path": "/path/0", "parents": ["/path/2"], "children": []},
    ...     {"path": "/path/1", "parents": [], "children": ["/path/2"]},
    ...     {"path": "/path/2", "parents": ["/path/1"],
    ...      "children": ["/path/0"]}]
    True

    Remove node_list[1]'s children.

    >>> node_list = [
    ...     {"path": "/path/0", "parents": [], "children": ["/path/1"]},
    ...     {"path": "/path/1", "parents": ["/path/0"],
    ...      "children": ["/not/exist"]}]
    >>> validate_link(node_list, node_list[1])
    >>> node_list == [
    ...     {"path": "/path/0", "parents": [], "children": ["/path/1"]},
    ...     {"path": "/path/1", "parents": ["/path/0"], "children": []}]
    True

    """
    path = node["path"]

    def validate(check_key):
        against_key = {"parents": "children", "children": "parents"}[check_key]
        link_path_list = []
        for link_path in node[check_key]:
            link_node = get(node_list, link_path)
            if link_node:
                link_path_list.append(link_path)
                if path not in link_node[against_key]:
                    link_node[against_key].append(path)
        node[check_key] = link_path_list

    validate("parents")
    validate("children")


def change_path(node_list, from_path, to_path):
    """
    Change node path.

    Parameters
    ----------
    from_path : str
        The path of node.
    to_path : str
        The destination path of node.

    Returns
    -------
    node_list

    Raises
    ------
    DataProcessorError
        If node 'to_path' is already registered
        or node with 'from_path' is not registered.

    """

    frm_p = utility.abspath(from_path)
    target_node = get(node_list, frm_p)
    if not target_node:
        raise DataProcessorError(
            "There is no node with the from_path %s." % frm_p)
    to_p = utility.abspath(to_path)
    if get(node_list, to_p):
        raise DataProcessorError(
            "The distination path %s is already registered." % to_p)

    target_node["path"] = to_p
    validate_link(node_list, target_node)
    for check_path in target_node["children"]:
        validate_link(node_list, get(node_list, check_path))
    for check_path in target_node["parents"]:
        validate_link(node_list, get(node_list, check_path))

    return node_list
