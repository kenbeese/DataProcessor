# coding=utf-8
import os
import shutil
import hashlib


class DataProcessorFigureError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


def create_node(figure_path, incidentals_path, parents, base_dir):
    """
    copy figure and incidentals and return corresponding node
    """
    path = copy(figure_path, incidentals_path, base_dir)
    return node(figure_path, parents, base_dir, path)


def node(figure_path, parents, base_dir, path=None):
    """
    Return node (does not copy)
    """
    if not path:
        path = _generate_path(figure_path, base_dir)
    _check_path(path)
    return {
        "path": path,
        "type": "figure",
        "name": os.path.basename(figure_path),
        "parents": parents,
        "children": [],
    }


def copy(fig_path, incidentals_path, base_dir):
    """
    copy figure and incidentals
    """
    _check_path(fig_path)
    dest_path = _generate_path(fig_path, base_dir)
    os.mkdir(dest_path)
    shutil.copy2(fig_path, dest_path)
    for inc_path in incidentals_path:
        shutil.copy2(inc_path, dest_path)
    return dest_path


zero_hash = hashlib.sha1("")
def calc_hash(figure_path):
    hash_str = hashlib.sha1(open(figure_path, 'r').read()).hexdigest()
    if hash_str == zero_hash:
        raise DataProcessorFigureError("Figure is empty.")
    return hash_str


def _generate_path(figure_path, base_dir):
    hash_str = calc_hash(figure_path)
    dest_path = os.path.join(base_dir, hash_str)
    if os.path.exists(dest_path):
        raise DataProcessorFigureError("Directory %s already exists."
                                       % dest_path)
    return dest_path


def _check_path(path):
    if not os.path.exists(path):
        raise DataProcessorFigureError("Path %s is not found." % path)


def _path_expand(path):
    return os.path.expanduser(os.path.abspath(path))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
