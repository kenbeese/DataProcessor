# -*- coding: utf-8 -*-

import os.path as op
import psutil
import json
from .utility import check_file
from .exception import DataProcessorError as dpError


class DataProcessorIpynbError(dpError):

    """Exception about IPython Notebook."""

    def __init__(self, msg):
        dpError.__init__(self, msg)


def gather_servers():
    """ Gather processes of IPython Notebook Server.

    Return
    ------
    notes : list of dict
        each dict has following keys: "pid", "cwd", and "port"

    Raises
    ------
    DataProcessorIpynbError
        - No IPython Notebook Server found
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
        raise DataProcessorIpynbError("No IPython Notebook Server found")
    return notes


def resolve_url(ipynb_path, servers=None):
    """
    Return valid URL for .ipynb.

    Parameters
    ----------
    ipynb_path : str
        path of existing .ipynb file
    servers : list, optional
        list of the information of notebook servers, which is
        got from "gather_servers". When this is specified, skip
        "gather_servers".(default=None)

    Raises
    ------
    DataProcessorIpynbError
        - Existing notebook servers do not start
          on the parent directory of .ipynb file.
    """
    ipynb_path = check_file(ipynb_path)
    if servers is None:
        servers = gather_servers()
    for server in servers:
        cwd = server["cwd"]
        if cwd.endswith("/"):
            cwd = cwd[:-1]
        if not ipynb_path.startswith(cwd):
            continue
        server["postfix"] = ipynb_path[len(cwd) + 1:]  # remove '/'
        return "http://localhost:{port}/notebooks/{postfix}".format(**server)
    raise DataProcessorIpynbError("""No valid IPython Notebook Server found.
    Please stand notebook server on the parent directory.""")


def resolve_name(ipynb_path):
    ipynb_path = check_file(ipynb_path)
    try:
        with open(ipynb_path, "r") as f:
            name = json.load(f)["metdata"]["name"]
    except KeyError:
        name = ""
    if not name:
        name = op.basename(ipynb_path)
    return name
