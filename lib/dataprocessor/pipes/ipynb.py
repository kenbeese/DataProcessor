# -*- coding: utf-8 -*-


import psutil
from subprocess import call
from ..utility import check_file
from ..exception import DataProcessorError as dpError


def gather_notebooks():
    """ Gather processes of IPython Notebook
    """
    notes = []
    for pid in psutil.pids():
        p = psutil.Process(pid)
        if p.name()[:7] != "ipython":
            continue
        if "notebook" not in p.cmdline():
            continue
        notes.append({
            "pid": pid,
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


def start_ipynb(nl, ipynb_path):
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

    """
    ipynb_path = check_file(ipynb_path)
    for note in gather_notebooks():
        cwd = note["cwd"]
        if ipynb_path[:len(cwd)] != cwd:
            continue
        note["postfix"] = ipynb_path[len(cwd)+1:]  # remove '/'
        retcode = call([
            "open",
            "http://{ip}:{port}/notebooks/{postfix}".format(**note)
        ])
        if retcode:
            raise dpError("Unknown error while opening notebook"
                          " (return code={})".format(retcode))
        return nl
    raise dpError("No valid Notebook found. "
                  "Please stand notebook server on the parent directory.")


def register(pipes_dics):
    pipes_dics["start_ipynb"] = {
        "func": start_ipynb,
        "args": ["ipynb_path"],
        "desc": "start .ipynb in standing notebook",
    }
