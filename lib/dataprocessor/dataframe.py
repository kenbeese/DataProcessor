# coding=utf-8

from pandas import DataFrame, Series
from . import utility
from .exception import DataProcessorError


def get_projects(node_list):
    """Get projects in dataframe format.

    Returns
    -------
    projects_dataframe : pandas.DataFrame

    """
    df = DataFrame(node_list)
    projects = df[df["type"] == "project"]
    return projects.dropna(how='all', axis=1)


def get_project(node_list, project_path, properties=["comment", "tags"],
                index="path"):
    """Get project in dataframe format.

    If there are two or more project of specified name,
    the latter one is selected.

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

    """
    project_path = utility.path_expand(project_path)
    df = DataFrame(node_list)
    runs_pre = df[df['parents'].apply(lambda val: project_path in val)]
    if len(runs_pre) == 0:
        raise DataProcessorError("There is no project of specified path :"
                                 + project_path)
    for item in ["name", "path"]:
        if item not in properties:
            properties.append(item)

    def _conv(val):
        sr = Series(val["configure"])
        for prop in properties:
            sr.set_value(prop, val[prop])
        return sr
    runs = runs_pre.apply(_conv, axis=1)
    runs = runs.convert_objects(convert_numeric=True)
    if index:
        runs = runs.set_index(index)
    return runs.dropna(how="all", axis=1)
