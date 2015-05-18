# -*- coding: utf-8 -*-

from . import rc, utility

import os
import os.path as op


def _get_basket(key, default_value):
    root = rc.get_configure(rc.rc_section, "root")
    utility.check_or_create_dir(root)
    basket_name = rc.get_configure_safe(rc.rc_section, key, default_value)
    basket = op.join(root, basket_name)
    utility.check_or_create_dir(basket)
    return basket


def get_project_basket():
    return _get_basket("project_basket", "Projects")


def get_run_basket():
    return _get_basket("run_basket", "Runs")


def get_tag_abspath(tag_name):
    """ Get abspath of the corresponding directory from tag name

    Parameters
    ----------
    tag_name : str
        name of tag
    root : str, optional
        The root path of baskets.
        If None, the path is read from the configure file.
    basket_name : str, optional
        The name of the project basket.
        If "project_basket" is specified in the configure file,
        default value is it. Otherwise, default is "Projects".

    Returns
    -------
    path : str

    """
    basket = get_project_basket()
    path = os.path.join(basket, tag_name)
    return path


def resolve_project_path(tagname_or_path):
    """ Autodetect tagname or path and return its abspath

    Parameters
    ----------
    tagname_or_path : str
        Project identifier.
        If tagname, call get_tag_abspath,
        If path, call utility.abspath

    Returns
    -------
    path : str

    """
    def _is_tag(s):
        if "/" in s:  # path
            return False
        if s[0] is ".":  # relative path
            return False
        return True
    if _is_tag(tagname_or_path):
        return get_tag_abspath(tagname_or_path)
    else:
        return utility.abspath(tagname_or_path)


def get_new_run_abspath(run_name):
    """ Generate abspath of a new run"""
    basket = get_run_basket()
    path = os.path.join(basket, run_name)
    return path
