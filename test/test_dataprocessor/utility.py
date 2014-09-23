# coding=utf-8
"""Utility of test."""

import unittest
import tempfile
import os
import sys
import shutil

sys.path = [sys.path[0]] \
    + [os.path.join(os.path.dirname(__file__), "../../../lib")] \
    + sys.path[1:]
import dataprocessor.nodes as nodes
sys.path = [sys.path[0]] + sys.path[2:]


class TestNodeListAndDir(unittest.TestCase):

    """Unittest for using node_list and directory.

    create node_list including following nodes.


    ============    =========  ========
    path            node_type  name
    ============    =========  ========
    tmpdir          project    tmpdir
    tmpdir/run01    run        run01
    tmpdir/run02    run        run02
    tmpdir/run03    run        run03
    ============    =========  ========

    Attributes
    ----------
    tempdir_paths : list
        list of project root dir path
    node_list : list
    rundir_nums : list
        number list of rundir in `tempdir_paths`

    """

    def setUp(self):
        self.tempdir_paths = []
        self.rundir_nums = []
        self.node_list = []
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
        rundir_num : int, optional
            number of rundir

        """

        self.rundir_nums.append(rundir_num)
        self.tempdir_paths.append(tempfile.mkdtemp())
        for tempdir_path in self.tempdir_paths:
            node = {"path": tempdir_path,
                    "type": "project",
                    "name": os.path.basename(tempdir_path),
                    "children": [],
                    "parents": [], }
            nodes.add(self.node_list, node)

            for i in range(rundir_num):
                path = os.path.join(tempdir_path, "run%02d" % i)
                os.mkdir(path)
                node = {"path": path,
                        "type": "run",
                        "name": os.path.basename(path),
                        "children": [],
                        "parents": [tempdir_path]}
                nodes.add(self.node_list, node)
