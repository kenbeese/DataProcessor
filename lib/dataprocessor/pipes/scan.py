# coding=utf-8
import os
from glob import glob

from ..nodes import get, validate_link


def directory(node_list, root, whitelist):
    """
    Search nodes from all directories under the directory 'root'.

    Run node has one or more file or directory
    which satisfies node_dir/whitelist.
    Project node has run node in its sub-directory.


    >>> scandir = "/tmp/scan_dir"
    >>> _generate_test_directories(scandir)
    >>> _show_test_directories(scandir)
    ('/tmp/scan_dir', ['run0', 'run1', 'run2', 'run3'], [])
    ('/tmp/scan_dir/run0', ['run0', 'run1'], ['test.conf'])
    ('/tmp/scan_dir/run0/run0', ['data'], [])
    ('/tmp/scan_dir/run0/run0/data', [], ['hoge.conf'])
    ('/tmp/scan_dir/run0/run1', [], ['test.conf'])
    ('/tmp/scan_dir/run1', [], ['test.conf'])
    ('/tmp/scan_dir/run2', [], ['test.conf'])
    ('/tmp/scan_dir/run3', ['data'], [])
    ('/tmp/scan_dir/run3/data', [], ['test.conf'])
    >>> directory([], scandir, ["*.conf"]) == [
    ...     {'path': '/tmp/scan_dir',
    ...      'parents': [],
    ...      'children': ['/tmp/scan_dir/run0',
    ...                   '/tmp/scan_dir/run1',
    ...                   '/tmp/scan_dir/run2'],
    ...      'name': 'scan_dir',
    ...      'type': 'project'},
    ...     {'path': '/tmp/scan_dir/run0',
    ...      'parents': ['/tmp/scan_dir'],
    ...      'children': ['/tmp/scan_dir/run0/run1'],
    ...      'name': 'run0',
    ...      'type': 'run'},
    ...     {'path': '/tmp/scan_dir/run0/run0',
    ...      'parents': [],
    ...      'children': ['/tmp/scan_dir/run0/run0/data'],
    ...      'name': 'run0',
    ...      'type': 'project'},
    ...     {'path': '/tmp/scan_dir/run0/run0/data',
    ...      'parents': ['/tmp/scan_dir/run0/run0'],
    ...      'children': [],
    ...      'name': 'data',
    ...      'type': 'run'},
    ...     {'path': '/tmp/scan_dir/run0/run1',
    ...      'parents': ['/tmp/scan_dir/run0'],
    ...      'children': [],
    ...      'name': 'run1',
    ...      'type': 'run'},
    ...     {'path': '/tmp/scan_dir/run1',
    ...      'parents': ['/tmp/scan_dir'],
    ...      'children': [],
    ...      'name': 'run1',
    ...      'type': 'run'},
    ...     {'path': '/tmp/scan_dir/run2',
    ...      'parents': ['/tmp/scan_dir'],
    ...      'children': [],
    ...      'name': 'run2',
    ...      'type': 'run'},
    ...     {'path': '/tmp/scan_dir/run3',
    ...      'parents': [],
    ...      'children': ['/tmp/scan_dir/run3/data'],
    ...      'name': 'run3',
    ...      'type': 'project'},
    ...     {'path': '/tmp/scan_dir/run3/data',
    ...      'parents': ['/tmp/scan_dir/run3'],
    ...      'children': [],
    ...      'name': 'data',
    ...      'type': 'run'}
    ... ]
    True
    >>> directory([], scandir, ["data"]) == [
    ...     {'path': '/tmp/scan_dir',
    ...      'parents': [],
    ...      'children': ['/tmp/scan_dir/run3'],
    ...      'name': 'scan_dir',
    ...      'type': 'project'},
    ...     {'path': '/tmp/scan_dir/run0',
    ...      'parents': [],
    ...      'children': ['/tmp/scan_dir/run0/run0'],
    ...      'name': 'run0',
    ...      'type': 'project'},
    ...     {'path': '/tmp/scan_dir/run0/run0',
    ...      'parents': ['/tmp/scan_dir/run0'],
    ...      'children': [],
    ...      'name': 'run0',
    ...      'type': 'run'},
    ...     {'path': '/tmp/scan_dir/run3',
    ...      'parents': ['/tmp/scan_dir'],
    ...      'children': [],
    ...      'name': 'run3',
    ...      'type': 'run'}
    ... ]
    True
    >>> directory([], scandir, ["data/hoge*", "data/test*"]) == [
    ...     {'path': '/tmp/scan_dir',
    ...      'parents': [],
    ...      'children': ['/tmp/scan_dir/run3'],
    ...      'name': 'scan_dir',
    ...      'type': 'project'},
    ...     {'path': '/tmp/scan_dir/run0',
    ...      'parents': [],
    ...      'children': ['/tmp/scan_dir/run0/run0'],
    ...      'name': 'run0',
    ...      'type': 'project'},
    ...     {'path': '/tmp/scan_dir/run0/run0',
    ...      'parents': ['/tmp/scan_dir/run0'],
    ...      'children': [],
    ...      'name': 'run0',
    ...      'type': 'run'},
    ...     {'path': '/tmp/scan_dir/run3',
    ...      'parents': ['/tmp/scan_dir'],
    ...      'children': [],
    ...      'name': 'run3',
    ...      'type': 'run'}
    ... ]
    True
    >>> import shutil
    >>> shutil.rmtree(scandir)
    """

    root = os.path.abspath(os.path.expanduser(root))
    scan_nodelist = []
    for path, dirs, files in os.walk(root):
        dirs.sort()
        node_type = None
        parents = []
        children = []
        if not get(node_list, path) is None:
                continue
        for child in dirs:
            for white in whitelist:
                if glob(os.path.join(path, child, white)):
                    node_type = "project"
                    children.append(os.path.join(path, child))
                    break
        for white in whitelist:
            if glob(os.path.join(path, white)):
                node_type = "run"
                parents.append(os.path.dirname(path))
                break
        if not node_type:
            continue
        scan_nodelist.append({"path": path,
                              "parents": parents,
                              "children": children,
                              "type": node_type,
                              "name": os.path.basename(path),
                              })
    node_list = node_list + scan_nodelist
    return node_list


def register(pipe_dics):
    pipe_dics["scan_directory"] = {
        "func": directory,
        "args": ["root_path", "whitelist"],
        "desc": "scan direcoty structure",
    }


def _generate_test_directories(root):
    os.mkdir(root)
    for i in range(4):
        os.mkdir(os.path.join(root, "run" + str(i)))
    for i in range(3):
        open(os.path.join(root, "run" + str(i), "test.conf"),
             "w").close()
    for i in range(2):
        os.mkdir(os.path.join(root, "run0", "run" + str(i)))
    os.mkdir(os.path.join(root, "run3", "data"))
    os.mkdir(os.path.join(root, "run0", "run0", "data"))
    open(os.path.join(root, "run0", "run1", "test.conf"), "w").close()
    open(os.path.join(root, "run3", "data", "test.conf"), "w").close()
    open(os.path.join(root, "run0", "run0", "data", "hoge.conf"),
         "w").close()


def _show_test_directories(root):
    for root, dirs, files in os.walk(root):
        dirs.sort()
        print((root, dirs, files))
