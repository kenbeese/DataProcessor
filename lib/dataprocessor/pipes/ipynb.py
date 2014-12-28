# -*- coding: utf-8 -*-


import psutil
import webbrowser
from ..utility import check_file
from ..exception import DataProcessorError as dpError


def gather_notebooks():
    """ Gather processes of IPython Notebook
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


def start(nl, ipynb_path):
    """
    Start existing .ipynb file
    at standing ipython notebook server

    Parameters
    ----------
    ipynb_path : str
        path of existing .ipynb file

    Raise
    -----
    DataProcessorError
        - No IPython Notebook found
        - Existing notebook servers do not start
          on the parent directory of .ipynb file.
        - Cannot open browser

    """
    ipynb_path = check_file(ipynb_path)
    for note in gather_notebooks():
        cwd = note["cwd"]
        if not ipynb_path.startswith(cwd):
            continue
        note["postfix"] = ipynb_path[len(cwd) + 1:]  # remove '/'
        url = "http://localhost:{port}/notebooks/{postfix}".format(**note)
        try:
            webbrowser.open(url)
        except webbrowser.Error:
            raise dpError("Unknown error while opening notebook")
        return nl
    raise dpError("No valid Notebook found. "
                  "Please stand notebook server on the parent directory.")


def register(pipes_dics):
    pipes_dics["start_ipynb"] = {
        "func": start,
        "args": ["ipynb_path"],
        "desc": "start .ipynb in standing notebook",
    }
