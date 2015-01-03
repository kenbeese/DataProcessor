# -*- coding: utf-8 -*-

import psutil
from .utility import check_file
from .exception import DataProcessorError as dpError


def gather_notebooks():
    """ Gather processes of IPython Notebook

    Return
    ------
    notes : list of dict
        each dict has following keys: "pid", "cwd", and "port"

    Raises
    ------
    DataProcessorError
        - No IPython Notebook found
    """
    notes = []
    for p in psutil.process_iter():
        if not p.name().lower() in ["ipython", "python"]:
            continue
        if "notebook" not in p.cmdline():
            continue
        for net in p.connections(kind="inet4"):
            if net.status != "LISTEN":
                continue
            _, port = net.laddr
            break
        notes.append({
            "pid": p.pid,
            "cwd": p.cwd(),
            "port": port,
        })
    if not notes:
        raise dpError("No IPython Notebook found")
    return notes


def resolve_url(ipynb_path):
    """
    Return valid URL for .ipynb

    Parameters
    ----------
    ipynb_path : str
        path of existing .ipynb file

    Raises
    ------
    DataProcessorError
        - Existing notebook servers do not start
          on the parent directory of .ipynb file.
    """
    ipynb_path = check_file(ipynb_path)
    for note in gather_notebooks():
        cwd = note["cwd"]
        if cwd.endswith("/"):
            cwd = cwd[:-1]
        if not ipynb_path.startswith(cwd):
            continue
        note["postfix"] = ipynb_path[len(cwd) + 1:]  # remove '/'
        return "http://localhost:{port}/notebooks/{postfix}".format(**note)
    raise dpError("No valid Notebook found. "
                  "Please stand notebook server on the parent directory.")
