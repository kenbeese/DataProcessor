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


def _check_child(child_path, node_list):
    for child_node in node_list:
        if child_path == child_node["path"]:
            return child_node
    return None


def add(node_list, pre_meta=["name", "date"],
        post_meta=["tags", "comment"], confs=None):
    """
    Add children information table to node as 'table' key.


    >>> add([
    ...     {"path": "/tmp/project",
    ...      "children": ["/tmp/run1", "/tmp/run0"]},
    ...     {"path": "/tmp/run0", "name": "run0",
    ...      "tags": ["run0_tag"], "comment": "test",
    ...      "configure": {"nx": 1, "ny": 2}},
    ...     {"path": "/tmp/run1", "name": "run1",
    ...      "tags": ["tag2", "tag3"],
    ...      "configure": {"nx": 10, "ny": 20}},
    ...     ],
    ...     pre_meta=["name"], post_meta=["tags", "comment"],
    ...    )[0] == {
    ...      'path': '/tmp/project', 'children': ['/tmp/run1', '/tmp/run0'],
    ...      'table': [{'comment': ['test', None], 'name': ['run0', 'run1'],
    ...                'path': ['/tmp/run0', '/tmp/run1'],
    ...                'tags': [['run0_tag'], ['tag2', 'tag3']],
    ...                'header': ['name', 'nx', 'ny', 'tags', 'comment'],
    ...                'nx': [1, 10], 'ny': [2, 20]}]}
    True
    """
    for node in node_list:
        if not "children" in node:
            continue
        table = {}
        config = confs
        for child_path in sorted(node["children"]):
            child = _check_child(child_path, node_list)
            if child is None:
                continue
            for key in set(pre_meta + post_meta + ["path"]):
                table = _copy_value(table, child, key)
            if not "configure" in child:
                continue
            if config is None:
                config = _get_confs(child)
            for key in config:
                table = _copy_value(table, child["configure"], key)
        if config is None:
            config = []
        table["header"] = pre_meta + config + post_meta
        if not "table" in node:
            node["table"] = [table]
        else:
            node["table"].append(table)
    return node_list


def register(pipes_dics):
    pipes_dics["add_children_table"] = {
        "func": add,
        "args": [],
        "desc": "add children information table",
        "kwds": ["pre_meta", "post_meta", "confs"],
        }


def _test():
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    _test()
