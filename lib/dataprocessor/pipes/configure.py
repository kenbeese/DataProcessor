# coding=utf-8
import os.path
from ConfigParser import SafeConfigParser

from ..utility import read_configure

def add(node_list, filename, section="parameters"):
    """
    Add configure to node_list.

    Parameters
    ----------
    filename : str
        filename of parameter configure file
        If file is not exists, add null list.

    section : str
        Specify section name in configure file.

    Examples
    ----------
    Create directory and file

    >>> import os
    >>> os.mkdir("/tmp/run01/")
    >>> os.mkdir("/tmp/run02/")
    >>> filestring = '''[conf]
    ... conf1 = 21
    ... conf2 = 1
    ... '''
    >>> f = open("/tmp/run01/parameter.conf", "w")
    >>> f.write(filestring)
    >>> f.close()
    >>> filestring = '''[conf]
    ... conf3 = 100
    ... '''
    >>> f = open("/tmp/run01/parameter2.conf", "w")
    >>> f.write(filestring)
    >>> f.close()

    Create node_list

    >>> node_list = [
    ...     {"path": "/tmp/run01/", "type": "run"},
    ...     {"path": "/tmp/run02", "type": "run"},
    ...     {"path": "/tmp/", "type": "project"}]

    Use `add`

    >>> new_node_list = add(node_list, "parameter.conf", "conf")
    >>> new_node_list == [
    ...     {"path": "/tmp/run01/", "type": "run",
    ...         "configure": {"conf1": "21", "conf2": "1"}},
    ...     {"path": "/tmp/run02", "type": "run",
    ...         "configure": {}},
    ...     {"path": "/tmp/", "type": "project"}]
    True
    >>> new_node_list = add(new_node_list, "parameter2.conf", "conf")
    >>> new_node_list == [
    ...     {"path": "/tmp/run01/", "type": "run",
    ...         "configure": {"conf1": "21", "conf2": "1", "conf3": "100"}},
    ...     {"path": "/tmp/run02", "type": "run",
    ...         "configure": {}},
    ...     {"path": "/tmp/", "type": "project"}]
    True

    Clean test environment

    >>> os.remove("/tmp/run01/parameter.conf")
    >>> os.remove("/tmp/run01/parameter2.conf")
    >>> os.rmdir("/tmp/run01/")
    >>> os.rmdir("/tmp/run02/")
    """

    new_list = []
    node_key = "configure"
    for node in node_list:
        if node["type"] == "run":
            confpath = os.path.join(node["path"], filename)
            conf_d = {}
            if os.path.exists(confpath):
                conf = SafeConfigParser()
                conf.optionxform = str
                conf.read(confpath)
                for key, var in conf.items(section):
                    conf_d[key] = var
            else:
                Warning("parameter file is not exists.")
            if not node_key in node:
                node[node_key] = conf_d
            else:
                for key in conf_d:
                    if key in node[node_key]:
                        Warning("overwrite configures")
                node[node_key].update(conf_d)

        new_list.append(node)
    return new_list


def no_section(node_list, filename, split_char="=", comment_char=["#"]):
    for node in node_list:
        path = node["path"]
        cfg_path = os.path.join(path, filename)
        if not os.path.exists(cfg_path):
            continue
        cfg = read_configure(cfg_path, split_char, comment_char)
        if "configure" not in node:
            node["configure"] = {}
        node["configure"].update(cfg)
    return node_list


def register(pipes_dics):
    pipes_dics["configure"] = {
        "func": add,
        "args": ["filename"],
        "kwds": ["section"],
        "desc": "Read parameter file (use ConfigParser)",
    }
    pipes_dics["configure_no_section"] = {
        "func": no_section,
        "args": ["filename"],
        "kwds": ["split_char", "comment_char"],
        "desc": "Read parameter file (without section)",
    }


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
