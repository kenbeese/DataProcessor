# coding=utf-8
"""Test for dataprocessor.pipes.configure."""

import os
import sys
import unittest
sys.path = [sys.path[0]] \
    + [os.path.join(os.path.dirname(__file__), "../../../lib")] \
    + sys.path[1:]
from dataprocessor.pipes.configure import add
sys.path = [sys.path[0]] + sys.path[2:]


class TestNodeListAndDir(unittest.TestCase):
    """Unittest for using node_list and directory.

    Attributes
    ----------
    tempdir_paths: list
        list of project root dir path
    node_list: list

    """

    def setUp(self):
        self._create_dir_and_node_list(rundir_num=3)

    def tearDown(self):
        import shutil
        for tempdir_path in self.tempdir_paths:
            shutil.rmtree(tempdir_path)

    def _create_dir_and_node_list(self, rundir_num=2):
        """Create test directory and node_list.

        Create one project directory and rundir_num rundirs.
        Add self.tempdir_paths to project dir path.

        parameters
        ----------
        rundir_num: int, optional
            number of rundir

        """

        import tempfile
        import os
        self.node_list = []
        self.tempdir_paths = [tempfile.mkdtemp(), ]
        for tempdir_path in self.tempdir_paths:
            node = {"path": tempdir_path,
                    "type": "project", }
            self.node_list.append(node)

            for i in range(rundir_num):
                path = os.path.join(tempdir_path, "run%02d" % i)
                os.mkdir(path)
                node = {"path": path,
                        "type": "run"}
                self.node_list.append(node)


class TestConfigure(TestNodeListAndDir):

    """Unittest for dataprocessor.pipes.configure.

    Attributes
    ----------
    tempdir_paths: list
        list of project root dir path
    node_list: list

    """
    def _create_conf_files(self, list_file_dict, check_type=False):
        """Create configure file on node path.

        Parameters
        ----------
        list_file_dict: list
            list of dict as follows,
            [{"name": "filename", "contents": "string of file contents"}, ]
        check_type: bool (False)
            If True, only create configure file on node with type run.

        """

        import os

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
        import copy
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
hgoe = 4
dsaf = ohd"""}]
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


if __name__ == '__main__':
    unittest.main()
