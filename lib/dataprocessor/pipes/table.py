# coding=utf-8


def _get_confs(node):
    confs = []
    for conf in node["configure"]:
        if conf not in confs:
            confs.append(conf)
    confs.sort()
    confs.sort(key=len)
    return confs


def _copy_value(dic_out, dic_in, key):
    if key in dic_in:
        value = dic_in[key]
    else:
        value = None
    if key in dic_out:
        dic_out[key].append(value)
    else:
        dic_out[key] = [value]
    return dic_out


def _check_path(path, node_list):
    for node in node_list:
        if path == node["path"]:
            return node
    return None


def add(node_list, table_type="children", pre_meta=["name", "date"],
        post_meta=["tags", "comment"], confs=None):
    """
    Add parents or children information table to 'widgets' key.

    >>> add([
    ...     {"path": "/tmp/project",
    ...      "children": ["/tmp/run1", "/tmp/run0"]},
    ...     {"path": "/tmp/run0", "name": "run0",
    ...      "comment": "test", "configure": {"nx": 1, "ny": 2}},
    ...     {"path": "/tmp/run1", "name": "run1",
    ...      "configure": {"nx": 10, "ny": 20}},
    ...     ],
    ...     table_type="children", pre_meta=["name"], post_meta=["comment"],
    ...    )[0] == {
    ...      'path': '/tmp/project', 'children': ['/tmp/run1', '/tmp/run0'],
    ...      'widgets': [{'type': 'table', 'tags': ['children'], 'data':
    ...          {'comment': ['test', None], 'name': ['run0', 'run1'],
    ...           'path': ['/tmp/run0', '/tmp/run1'],
    ...           'header': ['name', 'nx', 'ny', 'comment'],
    ...           'nx': [1, 10], 'ny': [2, 20]}}]}
    True
    """
    for node in node_list:
        if not table_type in node:
            continue
        widget = {"type": "table", "tags": [table_type]}
        data = {}
        config = confs
        for path in sorted(node[table_type]):
            linked_node = _check_path(path, node_list)
            if linked_node is None:
                continue
            for key in set(pre_meta + post_meta + ["path"]):
                data = _copy_value(data, linked_node, key)
            if not "configure" in linked_node:
                continue
            if config is None:
                config = _get_confs(linked_node)
            for key in config:
                data = _copy_value(data, linked_node["configure"], key)
        if not data:
            continue
        if config is None:
            config = []
        data["header"] = pre_meta + config + post_meta
        widget["data"] = data
        if not "widgets" in node:
            node["widgets"] = [widget]
        else:
            node["widgets"].append(widget)
    return node_list


def register(pipes_dics):
    pipes_dics["add_table"] = {
        "func": add,
        "args": [],
        "desc": "add parents or children information table as widget",
        "kwds": ["table_type", "pre_meta", "post_meta", "confs"],
        }


def _test():
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    _test()
