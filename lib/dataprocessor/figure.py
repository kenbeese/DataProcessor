# coding=utf-8
"""Handling node for figures."""
import os
import hashlib

from . import utility, nodes
from .exception import DataProcessorError


class DataProcessorFigureError(DataProcessorError):

    """Exception about figure."""

    def __init__(self, msg):
        DataProcessorError.__init__(self, msg)


def zero_hash():
    """ Return a SHA-1 hash of empty figure. """
    return hashlib.sha1("")


def calc_hash(figure_path):
    """ Return a SHA-1 hash of the figure. """
    return hashlib.sha1(open(figure_path, 'r').read()).hexdigest()


def destination_path(figure_path, figure_directory):
    """ Return the path of a directory where the figure will be copied.

    This is also an ID of the figure in DataProcessor.

    Parameters
    ----------
    figure_path : str
        The present path of figure
    figure_directory : str
        The path to `figure_directory`

    """
    figure_directory = utility.check_directory(figure_directory)
    hash_str = calc_hash(figure_path)
    return os.path.join(figure_directory, hash_str)


def new_node(figure_path, generators, figure_directory,
             parents, children=[]):
    """ Copy figure and incidentals and return corresponding node.

    Parameters
    ----------
    figure_path : str
        the present path of the figure
    generators : list
        the paths of files which should be managed with the figure
        s.t. gunplot file, python script, etc...
    figure_directory : str
        the base directory where figures are saved
    parents : list
        will be copied into node["parents"]
    children : list, optional
        will be copied into node["children"]

    Raises
    ------
    DataProcessorFigureError
        raised when the figure is empty

    """
    hash_str = calc_hash(figure_path)
    if hash_str == zero_hash():
        raise DataProcessorFigureError("Figure is empty")
    dest_path = destination_path(figure_path, figure_directory)
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    utility.copy_file(figure_path, dest_path)
    for gen in generators:
        gen_path = utility.check_file(gen)
        utility.copy_file(gen_path, dest_path)
    return {
        "path": dest_path,
        "type": "figure",
        "name": os.path.basename(figure_path),
        "parents": parents,
        "children": children,
    }


def register(node_list, figures, figure_directory, runs=[], generators=[]):
    """ Register figure into `node_list`.

    Parameters
    ----------
    node_list : list
        node_list
    figures : list
        the present paths of figures
    figure_directory : str
        the base directory where figures are saved
    runs : list
        The paths of runs related to these figures.
        They will be saved into node["parents"]
    generators : list
        the paths of files which should be managed with the figure;
        s.t. gunplot file, python script, etc...

    """
    figs = [utility.check_file(fig) for fig in figures]
    if runs:
        runs = [utility.check_directory(run) for run in runs]
    else:
        runs = [os.path.dirname(fig) for fig in figs]
    runs = list(set(runs))

    for fig in figs:
        try:
            node = new_node(fig, generators, figure_directory, runs)
        except DataProcessorFigureError, e:
            print(e)
            print("Skip %s" % fig)
            continue
        nodes.add(node_list, node)
