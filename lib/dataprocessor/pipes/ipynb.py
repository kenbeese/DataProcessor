# -*- coding: utf-8 -*-


import webbrowser
from ..ipynb import resolve_url


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
    url = resolve_url(ipynb_path)
    try:
        webbrowser.open(url)
    except webbrowser.Error:
        raise dpError("Unknown error while opening notebook")
    return nl


def register(pipes_dics):
    pipes_dics["start_ipynb"] = {
        "func": start,
        "args": ["ipynb_path"],
        "desc": "start .ipynb in standing notebook",
    }
