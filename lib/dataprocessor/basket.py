# -*- coding: utf-8 -*-

from . import rc, utility

import os
import os.path as op


def _ready_basket(root, basket_name):
    if not root:
        root = rc.get_configure(rc.rc_section, "root")
    root = utility.check_directory(root)
    return utility.get_directory(op.join(root, basket_name))


def resolve_project_path(name_or_path, create_dir, root=None,
                         basket_name=rc.get_configure_safe(rc.rc_section, "project_basket", "Projects")):
    """ Resolve project path from its path or name.

    Parameters
    ----------
    name_or_path : str
        Project identifier.
        If name (i.e. basename(name_or_path) == name_or_path),
        abspath of `root/basket_name/name` is returned.
        If path (otherwise case), returns its abspath.
    create_dir : boolean
        This flag determine the behavior occured when there is no directory at
        the resolved path as follows:
        - if create_dir is True: create new directory
        - if create_dir is False: raise DataProcessorError
    root : str, optional
        The root path of baskets. (default=None)
        If None, the path is read from the configure file.
    basket_name : str, optional
        The name of the project basket.
        If "project_basket" is specified in the configure file,
        default value is it. Otherwise, default is "Projects".

    Returns
    -------
    path : str
        existing project path

    Raises
    ------
    DataProcessorRcError
        occurs when `root` is not specified and it cannot be loaded
        from the setting file.

    DataProcessorError
        occurs when create_dir is False and a path is not resolved.

    """
    def _is_name(s):
        if "/" in s:  # path
            return False
        if s[0] is ".":  # relative path
            return False
        return True
    if _is_name(name_or_path):
        name = name_or_path
        basket = _ready_basket(root, basket_name)
        path = os.path.join(basket, name)
    else:
        path = utility.path_expand(name_or_path)
    if create_dir:
        return utility.get_directory(path)
    else:
        return utility.check_directory(path)
