# coding=utf-8

import os
import os.path as op
from .. import pipe
from ..utility import abspath, check_file
from ..exception import DataProcessorError as dpError

# Directory to put symlinks
STATIC_DIR=op.join(op.dirname(op.abspath(__file__)),
                   "../../../server/static/images/links")

@pipe.type("run")
def scan(node, filename):
    """ Scan videos

    Add 'video' dict to each node if the video file specified in the argument
    exists. The dict has two properties: 'path' tells path to the video file and
    'link' tells name of the symlink.
    
    Parameters
    ----------
    filename : str
        relative path to the video file. e.g. foo.gif ../bar.mp4
    """
    videopath = abspath(op.join(node["path"], filename))
    if not op.exists(videopath):
        return node

    # Map path to filename
    linkname = videopath.replace("/", "%")
    node["video"] = {
        "path": videopath,
        "link": linkname
    }

    if not op.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)

    linkpath = op.join(STATIC_DIR, linkname)
    if not op.exists(linkpath):
        os.symlink(videopath, linkpath)

    return node


def register(pipes_dics):
    pipes_dics["scan_videos"] = {
        "func": scan,
        "args": ["filename"],
        "desc": "Find videos and create links.",
    }
