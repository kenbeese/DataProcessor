# coding=utf-8
"""Test for dataprocessor.pipes.configure."""

import os
import sys
import unittest
import copy

from ..utility import TestNodeListAndDir
sys.path = [sys.path[0]] \
    + [os.path.join(os.path.dirname(__file__), "../../../lib")] \
    + sys.path[1:]
from dataprocessor.pipes.configure import add, no_section
sys.path = [sys.path[0]] + sys.path[2:]


class TestConfigure(TestNodeListAndDir):

    """Unittest for dataprocessor.pipes.configure.

    Attributes
    ----------
    tempdir_paths : list
        list of project root dir path
    node_list : list

    """

    def _create_conf_files(self, list_file_dict, check_type=False):
        """Create configure file on node path.

        Parameters
        ----------
        list_file_dict : list
            list of dict as follows,
            [{"name": "filename", "contents": "string of file contents"}, ]
        check_type : bool (False)
            If True, only create configure file on node with type run.

        """

        def create_conf(conf_path, filestring):
            f = open(conf_path, "w")
            f.write(filestring)
            f.close()

        for node in self.node_list:
            if check_type and not (node["type"] is "run"):
                continue
            for file_dict in list_file_dict:
                    path = os.path.join(node["path"], file_dict["name"])
                    create_conf(path, file_dict["contents"])

    def _check_node_list(self, original_node_list, added_dict):
        compare_node_list = copy.deepcopy(original_node_list)
        for node in compare_node_list:
            node.update(added_dict)
        self.assertEqual(self.node_list, compare_node_list)

    def test_add(self):
        import copy
        original_node_list = copy.deepcopy(self.node_list)
        list_file_dict = [{"name": "parameter1.conf",
                           "contents": """[parameters]
hgoe = 3
hogehoge = 2"""},
                          {"name": "parameter2.conf",
                           "contents": """[default]
hgoe : 4
dsaf : ohd"""}]
        self._create_conf_files(list_file_dict)

        # there is no parameter.conf
        add(self.node_list, "parameter.conf", "parameters")
        added_dict = {"configure": {}}
        self._check_node_list(original_node_list, added_dict)

        # Add parameter1.conf to node_list
        add(self.node_list, "parameter1.conf", "parameters")
        added_dict = {"configure": {"hgoe": "3", "hogehoge": "2"}}
        self._check_node_list(original_node_list, added_dict)

        # Add parameter2.conf to added node_list
        add(self.node_list, "parameter2.conf", "default")
        added_dict = {"configure": {"hgoe": "4", "dsaf": "ohd",
                                    "hogehoge": "2"}}
        self._check_node_list(original_node_list, added_dict)

    def test_no_section(self):
        original_node_list = copy.deepcopy(self.node_list)
        list_file_dict = [{"name": "parameter1.conf",
                           "contents": """
# comment
hgoe = 3
hogehoge = 2"""},
                          {"name": "parameter2.conf",
                           "contents": """
! comment
hgoe :  4
dsaf : ohd"""}]
        self._create_conf_files(list_file_dict)

        # there is no parameter.conf
        no_section(self.node_list, "parameter.conf")
        added_dict = {}
        self._check_node_list(original_node_list, added_dict)

        # Add parameter1.conf to node_list
        no_section(self.node_list, "parameter1.conf")
        added_dict = {"configure": {"hgoe": "3", "hogehoge": "2"}}
        self._check_node_list(original_node_list, added_dict)

        # Add parameter2.conf to added node_list
        no_section(self.node_list, "parameter2.conf", ":", "!")
        added_dict = {"configure": {"hgoe": "4", "dsaf": "ohd",
                                    "hogehoge": "2"}}
        self._check_node_list(original_node_list, added_dict)
