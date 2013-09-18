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


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
