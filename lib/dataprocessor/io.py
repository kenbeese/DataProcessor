# coding=utf-8
from .exception import DataProcessorError
from . import utility, nodes

import json
import os
import os.path
import time
from logging import getLogger, DEBUG
logger = getLogger(__name__)
logger.setLevel(DEBUG)


def save(node_list, json_path):
    """Save node_list into a JSON file.

    Parameters
    ----------
    json_path : str
        the path to JSON

    Returns
    -------
    list : node_list

    """
    path = utility.abspath(json_path)
    if os.path.exists(path):
        logger.warning("File {} is overwritten.".format(json_path))
    with open(path, "w") as f:
        json.dump(node_list, f, indent=4)
    return node_list


def load(node_list, json_path):
    """Load node_list from a JSON file.

    Parameters
    ----------
    json_path : str
        the path to JSON

    Returns
    -------
    list
        node_list(arg1) + [new node list]

    Raises
    ------
    DataProcessorError
        occurs when JSON file does not exist.

    """
    path = utility.abspath(json_path)
    if not os.path.exists(path):
        raise DataProcessorError("JSON does not exist")
    with open(path, "r") as f:
        read_node_list = json.load(f)
    return node_list + read_node_list


class DataHandler(object):

    """ A data handler.

    A utility class for save/load data into/from JSON file.
    See the following example.
    This class use JSON format for serializing.

    Attributes
    ----------
    node_list : list
        the managed `node_list`

    Methods
    -------
    get()
        returns managed node_list
    add(node, skip_validate_link)
        add node into managed node_list
    replace(node_list, skip_validate_link)
        swap managed node_list and node_list in the argument
    serialize()
        serialize node_list into file.
        If you use `with` statement, you need not to call this.

    Examples
    --------
    >>> with DataHandler(filename) as dh:  # doctest: +SKIP
    ...     dh.add({"path" : "/path/to/data1", "name" : "data1",
    ...             "parents": [], "children": []})

    """

    def __init__(self, filename):
        self.data_path = utility.abspath(filename)
        self.load()

    def __enter__(self):
        self.load()  # reload
        return self

    def __exit__(self, exception_t, exception_v, traceback):
        if exception_t:
            return False
        self.serialize()
        return True

    def load(self):
        if os.path.exists(self.data_path):
            self.node_list = load([], self.data_path)
        else:
            logger.warning("File {} does not exists. Create new list".format(self.data_path))
            self.node_list = []

    def get(self):
        return self.node_list

    def add(self, node, strategy="update", skip_validate_link=False):
        """ Add node into managed node_list.

        Parameters
        ----------
        skip_validate_link : bool, optional
            skip link check (default=False)

        """
        nodes.add(self.node_list, node, strategy, skip_validate_link)

    def update(self, node_list, skip_validate_link=False):
        """ Update node_list (use nodes.modest_update).

        Parameters
        ----------
        skip_validate_link : bool, optional
            skip link validation about all nodes in new `node_list`
        """
        for node in node_list:
            nodes.add(self.node_list, node,
                      strategy="modest_update",
                      skip_validate_link=skip_validate_link)
        if skip_validate_link:
            return
        for node in node_list:
            nodes.validate_link(node_list, node)

    def replace(self, node_list, skip_validate_link=True):
        """ Swap node_list.

        Parameters
        ----------
        skip_validate_link : bool, optional
            skip link validation about all nodes in new `node_list`

        """
        self.node_list = node_list
        if not skip_validate_link:
            for node in self.node_list:
                nodes.validate_link(self.node_list, node)

    def serialize(self):
        save(self.node_list, self.data_path)


class SyncDataHandler(DataHandler):

    """ A synced data handler.

    This lock reading/writing JSON file.

    """

    def __init__(self, filename, lock_dir="/tmp", prefix="SyncDH", duration=0.1):
        DataHandler.__init__(self, filename)
        self.pid = os.getpid()
        self.lock_dir = os.path.join(lock_dir, prefix + utility.abspath(filename).replace("/", "_"))
        self.lock_fn = os.path.join(self.lock_dir, "pid")
        self.duration = duration

    def __enter__(self):
        while(True):
            if os.path.exists(self.lock_dir):
                with open(self.lock_fn, 'r') as f:
                    pid = int(f.read())
                logger.info("Waiting to lock {file:s} (PID={pid})".format(file=self.data_path, pid=pid))
                time.sleep(self.duration)
            else:
                os.mkdir(self.lock_dir)
                with open(self.lock_fn, 'w') as f:
                    f.write(str(self.pid))
                break
        return DataHandler.__enter__(self)

    def __exit__(self, type, value, traceback):
        with open(self.lock_fn, 'r') as f:
            pid = int(f.read())
        if pid != self.pid:
            raise DataProcessorError("PID missmatch")
        DataHandler.__exit__(self, type, value, traceback)
        os.remove(self.lock_fn)
        os.rmdir(self.lock_dir)
