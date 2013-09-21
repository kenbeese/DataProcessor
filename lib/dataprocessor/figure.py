# coding=utf-8
import os
import shutil
import hashlib


class DataProcessorFigureError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


def create_node(figure_path, incidentals_path, parents, base_dir,
                without_copy=False):
    if without_copy:
        path = _generate_path(figure_path, base_dir)
    else:
        path = _copy(figure_path, incidentals_path, base_dir)
    return {
        "path": path,
        "type": "figure",
        "name": os.path.basename(figure_path),
        "parents": parents,
        "children": [],
    }


def calc_hash(figure_path):
    return hashlib.sha1(open(figure_path, 'r').read()).hexdigest()


def _copy(fig_path, incidentals_path, base_dir):
    _check_path(fig_path)
    dest_path = _generate_path(fig_path, base_dir)
    os.mkdir(dest_path)
    shutil.copy2(fig_path, dest_path)
    for inc_path in incidentals_path:
        shutil.copy2(inc_path, dest_path)
    return dest_path


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
