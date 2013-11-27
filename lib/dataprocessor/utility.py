# coding=utf-8
"""Utility of dataprocessor.

Some useful tools for dataprocessor are included.

"""
from .exception import DataProcessorError
import os.path
import shutil


def path_expand(path):
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
        raise DataProcessorError("File '%s' does not exist" % path)
    if os.path.isdir(path):
        raise DataProcessorError("%s is not a file but a directory" % path)
    return path


def check_directory(path):
    """Check whether file exists.

    Returns
    -------
    str
        Absolute path of the argument

    Raises
    ------
    DataProcessorError
        occurs when the file does not exist or the file is not directory.

    """
    path = path_expand(path)
    if not os.path.exists(path):
        raise DataProcessorError("Directory '%s' does not exist" % path)
    if not os.path.isdir(path):
        raise DataProcessorError("%s is not a directory" % path)
    return path


def get_directory(path, silent=True):
    """Get absolute path of the directory.

    If it does not exist, it will be created.

    Parameters
    ----------
    silent : bool, optional
        does not ask whether create directory (default=True)

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


def copy_file(from_path, to_path):
    """ Copy a file. """
    from_path = check_file(from_path)
    to_path = path_expand(to_path)
    if os.path.exists(to_path) and os.path.isdir(to_path):
        to_dir = to_path
        to_name = os.path.basename(from_path)
    else:
        to_dir = os.path.dirname(to_path)
        to_name = os.path.basename(to_path)
    if not os.path.exists(to_dir):
        os.makedirs(to_dir)
    dest_path = os.path.join(to_dir, to_name)
    if not os.path.exists(dest_path):
        shutil.copy2(from_path, dest_path)
        return
    else:
        print("A file already exists in %s" % dest_path)
        from_con = open(from_path, 'r').read()
        dest_con = open(dest_path, 'r').read()
        if from_con == dest_con:
            print("They are same contents. Skip copy.")
            return
        else:
            while(True):
                ans = raw_input("Replace %s? [y/N]:" % dest_path)
                if ans.upper() in ["Y", "YES"]:
                    shutil.copy2(from_path, dest_path)
                    return
                else:
                    name = raw_input("Enter new name:")
                    new_dest = os.path.join(to_dir, name)
                    if os.path.exists(new_dest):
                        print("It also exits")
                        continue
                    else:
                        shutil.copy2(from_path, new_dest)
                        return


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
        lines = line.strip("\n").strip().split(split_char)
        if(len(lines) != 2):
            print("invalid line : "+line)
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
