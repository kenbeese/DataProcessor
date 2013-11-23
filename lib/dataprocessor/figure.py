# coding=utf-8
import os
import shutil
import hashlib

from . import utility, nodes
from .exception import DataProcessorError


class DataProcessorFigureError(DataProcessorError):
    def __init__(self, msg):
        DataProcessorError.__init__(self, msg)


def zero_hash():
    """ Return a SHA-1 hash of empty figure """
    return hashlib.sha1("")


def calc_hash(figure_path):
    """ Return a SHA-1 hash of the figure """
    return hashlib.sha1(open(figure_path, 'r').read()).hexdigest()


def destination_path(figure_path, figure_directory):
    """ Returns the path of a directory where the figure will be copied

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
    """ copy figure and incidentals and return corresponding node

    Parameters
    ----------
    figure_path : str
        the present path of the figure
    generators : list
        the paths of files which should be managed with the figure
        s.t. gunplot file, python script, etc...

    Raises
    ------
    DataProcessorFigureError
        raised in the following two cases:

        - the figure is empty
        - a same figure is already registered

    """
    hash_str = calc_hash(figure_path)
    if hash_str == zero_hash():
        raise DataProcessorFigureError("Figure is empty")
    dest_path = destination_path(figure_path, figure_directory)
    if os.path.exists(dest_path):
        raise DataProcessorFigureError("Same figure is already managed")
    os.mkdir(dest_path)
    shutil.copy2(figure_path, dest_path)
    for gen in generators:
        gen_path = utility.check_directory(gen)
        shutil.copy2(gen_path, dest_path)
    return {
        "path": dest_path,
        "type": "figure",
        "name": os.path.basename(figure_path),
        "parents": parents,
        "children": children,
    }


def register(node_list, figures, figure_directory, runs=[], generators=[]):
    """ register figure into `node_list`

    Parameters
    ----------
    figures : list
        the present paths of figures

    generators : list
        the paths of files which should be managed with the figure
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
