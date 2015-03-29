# coding=utf-8

from pandas import DataFrame
from . import utility
from . import nodes
from .exception import DataProcessorError as dpError


def get_projects(node_list):
    """Get projects in dataframe format.

    Returns
    -------
    projects_dataframe : pandas.DataFrame

    """
    df = DataFrame(node_list)
    projects = df[df["type"] == "project"]
    return projects.dropna(how='all', axis=1)


def get_project(node_list, project_path, properties=["comment"], index="path"):
    """ Get project dataframe
    i.e. the table of configures of runs which belongs the project

    Parameters
    ----------
    project_path : str
        the path of project
    properties : list of str (optional)
        properties successed from node_list into project dataframe
        "name" and "path" are successed always
        (Default=["comment", "tags"])
    index : str or list of str (optional)
        index of project dataframe
        if it is `None`, the index of DataFrame(node_list) will be successed
        (Default="path")

    Returns
    -------
    project : pandas.DataFrame

    Example
    -------
    >>> nl = [{
    ...     "path": "/path/p0",
    ...     "type": "project",
    ...     "parents": [],
    ...     "children": ["/path/c0", "/path/c1"],
    ... }, {
    ...     "path": "/path/c0",
    ...     "name": "c0",
    ...     "type": "run",
    ...     "configure": { "A": "1", },
    ...     "parents": ["/path/p0"],
    ...     "children": [],
    ... },{
    ...     "path": "/path/c1",
    ...     "name": "c1",
    ...     "type": "run",
    ...     "configure": { "A": "2", },
    ...     "parents": ["/path/p0"],
    ...     "children": [],
    ... }]
    >>> get_project(nl, "/path/p0")
              A name
    path            
    /path/c0  1   c0
    /path/c1  2   c1
    """
    def _append_if_not_exist(key):
        if key not in properties:
            properties.append(key)
    _append_if_not_exist("path")
    _append_if_not_exist("name")
    project_path = utility.path_expand(project_path)

    pnode = nodes.get(node_list, project_path)
    if not pnode:
        raise dpError("There is no project: " + project_path)

    run_nodes = []
    for p in pnode["children"]:
        n = nodes.get(node_list, p)
        if n["type"] != "run":
            continue
        if "configure" in n and isinstance(n["configure"], dict):
            cfg = _convert_to_float(n["configure"])
        else:
            cfg = {}
        for prop in properties:
            if prop in n:
                cfg[prop] = n[prop]
        run_nodes.append(cfg)
    df = DataFrame(run_nodes)
    if index and index in df.columns:
        df = df.set_index(index)
    return df


def _convert_to_float(configure):
    cfg = {}
    for k, v in configure.items():
        try:
            cfg[k] = float(v)
        except ValueError:
            cfg[k] = v
    return cfg
