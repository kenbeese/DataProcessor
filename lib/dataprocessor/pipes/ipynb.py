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
        if not p.name().startswith("ipython"):
            continue
        if "notebook" not in p.cmdline():
            continue
        notes.append({
            "pid": p.pid,
            "cwd": p.cwd(),
        })

    if not notes:
        raise dpError("No IPython Notebook found")

    for net in psutil.net_connections():
        if not net.pid or net.status != "LISTEN":
            continue
        ip, port = net.laddr
        if len(ip.split(".")) != 4:  # IPv4 only
            continue
        for note in notes:
            if net.pid == note["pid"]:
                note["ip"], note["port"] = net.laddr

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
        note["postfix"] = ipynb_path[len(cwd)+1:]  # remove '/'
        url = "http://{ip}:{port}/notebooks/{postfix}".format(**note)
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
