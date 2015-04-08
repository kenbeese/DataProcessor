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


def safe_float(val):
    try:
        return float(val)
    except ValueError:
        return val


def get_project(node_list, project_path, properties=["comment"], index="path"):
    """ Get project dataframe
    i.e. the table of configures of runs which belongs the project

    Parameters
    ----------
    project_path : str
        the path of project
    properties : list of str (optional)
        properties succeeded from node_list into project dataframe
        "name" and "path" are always succeeded
        (Default=["comment", "tags"])
    index : str or list of str (optional)
        index of project dataframe
        if it is `None`, the index of DataFrame(node_list) will be succeeded
        (Default="path")

    Raises
    ------
    DataProcessorError
        raised if the index is invalid

    Returns
    -------
    project : pandas.DataFrame

    """
    properties = set(properties)
    properties.add("path")
    properties.add("name")
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
            cfg = {k: safe_float(v) for k, v in n["configure"].items()}
        else:
            cfg = {}
        for prop in properties:
            if prop in n:
                cfg[prop] = n[prop]
        run_nodes.append(cfg)
    df = DataFrame(run_nodes)
    if not index:
        return df
    if isinstance(index, str):
        index = [index, ]
    if not isinstance(index, list):
        raise dpError("Invalid index {}".format(index))
    for idx in index:
        if idx not in df.columns:
            raise dpError("Invalid index: {}".format(idx))
    df = df.set_index(index)
    return df
