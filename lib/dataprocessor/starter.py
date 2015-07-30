# -*- coding: utf-8 -*-

from . import utility, basket, nodes
from .runner import runners
from .exception import DataProcessorError as dpError
import os.path
import shutil

from logging import getLogger, DEBUG
logger = getLogger(__name__)
logger.setLevel(DEBUG)


def copy_requirements(path, requirements):
    utility.check_dir(path)
    for req in requirements:
        utility.check_file(req)
        shutil.copy2(req, path)


def ready_projects(node_list, projects):
    projects = [basket.resolve_project_path(p) for p in projects]
    for project_path in projects:
        if nodes.get(node_list, project_path):  # already exists
            continue
        logger.info("Create new project node: {}".format(project_path))
        utility.check_or_create_dir(project_path)
        node = nodes.normalize({
            "path": project_path,
            "name": os.path.basename(project_path),
            "type": "project",
        })
        nodes.add(node_list, node)
    return projects


def start(node_list, args, requirements,
          name=utility.now_str(), projects=[], runner="sync"):
    """ Start run and register it into node_list

    Parameters
    ----------
    args : list of str
        arguments of run
    requirements : list of str
        list of paths which need to start run
    name : str, optional
        name of new run
    projects : list of str, optional
        tags or paths of projects (default=[])

    Return
    ------
    dict
        new node
    """
    path = basket.get_new_run_abspath(name)
    if os.path.exists(path):
        raise dpError("Already exists: {}".format(path))
    with utility.mkdir(path):
        copy_requirements(path, requirements)
        runners[runner](args, path)
    projects = ready_projects(node_list, projects)
    new_node = nodes.normalize({
        "path": path,
        "name": name,
        "type": "run",
        "parents": projects,
        "children": [],
    })
    nodes.add(node_list, new_node)
    return new_node
