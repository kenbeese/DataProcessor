# coding=utf-8
"""Utility of test."""

import unittest
import tempfile
import os
import shutil


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

        self.node_list = []
        self.tempdir_paths = [tempfile.mkdtemp(), ]
        for tempdir_path in self.tempdir_paths:
            node = {"path": tempdir_path,
                    "type": "project",
                    "name": os.path.basename(tempdir_path),
                    "children": [],
                    "parents": [], }
            self.node_list.append(node)

            for i in range(rundir_num):
                path = os.path.join(tempdir_path, "run%02d" % i)
                os.mkdir(path)
                node = {"path": path,
                        "type": "run",
                        "name": os.path.basename(path),
                        "children": [],
                        "parents": [], }
                self.node_list.append(node)
