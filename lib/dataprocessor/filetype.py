# -*- coding: utf-8 -*-

import enum
import os
import sys


FILETYPES = ["ini", "yaml"]
FileType = enum.Enum("FileType", "NONE " + " ".join(FILETYPES))


def guess_filetype_from_path(path):
    """
    Get filetype from path (filename extension).

    Parameters
    ----------
    path: str
        path to a file

    Returns
    -------
    FileType enum. If unknown filename extension is given, show warning
    """
    _, ext = os.path.splitext(path)

    # check extension in case insensitive way
    ext = ext.lower()
    if ext in (".ini", ".conf"):
        return FileType.ini
    elif ext in (".yml", ".yaml"):
        return FileType.yaml
    else:
        print >>sys.stderr, "Unknown ext '{}'".format(ext)
        return FileType.NONE
