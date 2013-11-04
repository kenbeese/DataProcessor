# coding=utf-8
from .exception import DataProcessorError
from . import utility, nodes

import json
import os.path


def save(node_list, json_path, silent=False):
    """save node_list into a JSON file

    Parameters
    ----------
    json_path : str
        the path to JSON
    slient : bool, str, optional
        Ask whether replace JSON file (default=False)
    """
    silent = utility.boolenize(silent)
    path = utility.path_expand(json_path)
    if not silent and os.path.exists(path):
        ans = raw_input("File %s already exists. Replace? [y/N]"
                        % json_path).lower()
        if ans not in ["yes", "y"]:
            print("Skip save_json pipe.")
            return node_list
    with open(path, "w") as f:
        json.dump(node_list, f, indent=4)
    return node_list


def load(node_list, json_path):
    """load node_list from a JSON file

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
    path = utility.path_expand(json_path)
    if not os.path.exists(path):
        raise DataProcessorError("JSON does not exist")
    with open(path, "r") as f:
        read_node_list = json.load(f)
    return node_list + read_node_list


class DataHandler(object):
    """ A data handler

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
    >>> filename = "/tmp/DataHandlerTest.json"
    >>> with DataHandler(filename, True) as dh:
    ...     dh.add({"path" : "/path/to/data1", "name" : "data1"}, True)
    >>> print(open(filename, 'r').read())
    [
        {
            "path": "/path/to/data1", 
            "name": "data1"
        }
    ]
    >>> import os; os.remove(filename)
    """
    def __init__(self, filename, silent=False):
        self.data_path = utility.path_expand(filename)
        self.silent = silent
        if os.path.exists(self.data_path):
            self.node_list = load([], self.data_path)
        else:
            print("Create new data in %s" % self.data_path)
            self.node_list = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.serialize()

    def get(self):
        return self.node_list

    def add(self, node, skip_validate_link=False):
        """ add node into managed node_list

        Parameters
        ----------
        skip_validate_link : bool, optional
            skip link check (default=False)
        """
        nodes.add(self.node_list, node, skip_validate_link)

    def replace(self, node_list, skip_validate_link=True):
        """ swap node_list

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
        save(self.node_list, self.data_path, self.silent)
