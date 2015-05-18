# coding=utf-8
"""Utility of dataprocessor.

Some useful tools for dataprocessor are included.

"""
from .exception import DataProcessorError
import os.path
import subprocess
from contextlib import contextmanager
from datetime import datetime


def abspath(path):
    """Get absolute path.

    Returns
    -------
    str
        Absolute path of the argument

    Raises
    ------
    DataProcessorError
        path is not readable

    """
    if type(path) not in [str, unicode]:
        raise DataProcessorError("path should be str or unicode: %s"
                                 % type(path))
    return os.path.abspath(os.path.expanduser(path))


def check_file(path):
    """ Check whether file exists.

    Raises
    ------
    DataProcessorError
        occurs in two cases:

        + when the file does not exist
        + file exist but it is a directory

    """
    if not os.path.exists(path):
        raise DataProcessorError("File '%s' does not exist" % path)
    if os.path.isdir(path):
        raise DataProcessorError("%s is not a file but a directory" % path)


def check_dir(path):
    """Check whether directory exists.

    Raises
    ------
    DataProcessorError
        occurs when the file does not exist or the file is not directory.

    """
    if not os.path.exists(path):
        raise DataProcessorError("Directory '%s' does not exist" % path)
    if not os.path.isdir(path):
        raise DataProcessorError("%s is not a directory" % path)


def check_or_create_dir(path):
    """ Check whether directory exists.
    If it does not exist, it will be created.

    Raises
    ------
    DataProcessorError
        occurs when another file (not directory) exist

    """
    if not os.path.isdir(path):
        if os.path.exists(path):
            raise DataProcessorError("Another file already exists in %s" % path)
        os.makedirs(path)


@contextmanager
def chdir(path):
    """ do in another directory and return previsous directory """
    cwd = os.getcwd()
    check_dir(path)
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(cwd)


@contextmanager
def mkdir(path):
    """ Create directory unless anything goes bad """
    os.mkdir(path)
    try:
        yield
    except Exception:
        os.rmdir(path)
        raise


def check_call(args, **kwds):
    try:
        subprocess.check_call(args, **kwds)
    except subprocess.CalledProcessError:
        raise DataProcessorError("Failed: {}".format(args))


def now_str(formatter="%FT%T"):
    return datetime.now().strftime(formatter)


def read_configure(filename, split_char="=", comment_char=["#"]):
    """ Read configure file without sections.

    Parameters
    ----------
    filename : str
        The file name of the configure file
    split_char : str, optional
        The lines in configure file are splited by this char (default "=").
        If your configure has line s.t. `a : 1.2`,
        then you should set `split_char=":"`.
    comment_char : list of str, optional
        The line starting with chars in this list will be skipped.
        (default=["#"])

    Returns
    -------
    dict
        {parameter-name: value} dictionary.

    """
    f = open(filename, 'r')
    config = {}
    for line in f:
        if line[0] in comment_char or line == "\n":
            continue
        lines = line.strip().split(split_char)
        if(len(lines) != 2):
            print("invalid line : " + line)
            continue
        config[lines[0].strip()] = lines[1].strip()
    return config


def boolenize(arg):
    """Make arg boolen value.

    Parameters
    ----------
    arg : bool, str, int, float

    Returns
    -------
    bool

    Examples
    --------
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
