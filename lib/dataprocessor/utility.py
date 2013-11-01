# coding=utf-8
from .exception import DataProcessorError
import os.path


def path_expand(path):
    """Get absolute path

    Returns
    -------
    str
        Absolute path of the argument
    """
    return os.path.expanduser(os.path.abspath(path))


def check_file(path):
    """Check whether file exists.

    Returns
    -------
    str
        Absolute path of the argument

    Raises
    ------
    DataProcessorError
        occurs in two cases:
        + when the file does not exist
        + file exist but it is a directory
    """
    path = path_expand(path)
    if not os.path.exists(path):
        raise DataProcessorError("File does not exist")
    if os.path.isdir(path):
        raise DataProcessorError("%s is not a file but a directory" % path)
    return path


def check_directory(path, silent=True):
    """Check whether the directory exists.

    If it does not exist, it will be created.

    Parameters
    ----------
    silent : bool, optional
        Ask whether create directory (default=True)

    Returns
    -------
    str
        Absolute path of the directory

    Raises
    ------
    DataProcessorError
        occurs in two cases
        + another file (does not directory) exist
        + refused by user to create directory
    """
    dir_path = path_expand(path)
    if not os.path.isdir(dir_path):
        if os.path.exists(dir_path):
            raise DataProcessorError("Another file already exists in %s"
                                     % dir_path)
        if not silent:
            ans = raw_input("Create directory(%s)? [y/N]" % dir_path)
            if ans not in ["yes", "y"]:
                raise DataProcessorError("Directory cannot be created.")
        os.makedirs(dir_path)
    return dir_path


def boolenize(arg):
    """make arg boolen value

    >>> boolenize(True)
    True
    >>> boolenize(False)
    False

    >>> boolenize(1)
    True
    >>> boolenize(0)
    False
    >>> boolenize(0.0)
    False

    >>> boolenize("True")
    True
    >>> boolenize("other words")
    True
    >>> boolenize("False")
    False
    >>> boolenize("falSE")
    False
    >>> boolenize("false")
    False
    >>> boolenize("F")
    False
    >>> boolenize("f")
    False
    >>> boolenize("No")
    False
    >>> boolenize("NO")
    False
    >>> boolenize("no")
    False
    >>> boolenize("N")
    False
    >>> boolenize("n")
    False
    """
    if type(arg) == str and arg.lower() in ["false", "f", "no", "n"]:
        return False
    return bool(arg)
