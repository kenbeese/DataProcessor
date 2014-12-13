# coding=utf-8
"""Utility of test."""

import unittest
import tempfile
import os
import shutil
from .. import nodes


class TestNodeListAndDir(unittest.TestCase):

    """Unittest for using node_list and directory.

    create node_list including following nodes.


    ===============   =========  ========
    path              node_type  name
    ===============   =========  ========
    tmpdir/p1         project    p1
    tmpdir/p1/run00   run        run00
    tmpdir/p1/run01   run        run01
    tmpdir/p1/run02   run        run02
    tmpdir/p2         project    p2
    tmpdir/p2/run00   run        run00
    tmpdir/p2/run01   run        run01
    ===============   =========  ========

    Attributes
    ----------
    tempdir_path : str
        temporally directory path
    project_paths : list
        list of project path
    node_list : list

    """

    def setUp(self):
        self.tempdir_path = tempfile.mkdtemp()
        self.project_paths = []
        self.node_list = []
        self._create_project_and_run("p1", rundir_num=3)
        self._create_project_and_run("p2", rundir_num=2)

    def tearDown(self):
        shutil.rmtree(self.tempdir_path)

    def _create_project_and_run(self, project_name, rundir_num=2):
        p_path = os.path.join(self.tempdir_path, project_name)
        self._create_project_or_run(p_path)

        for i in range(rundir_num):
            path = os.path.join(p_path, "run%02d" % i)
            self._create_project_or_run(path, type="run", parents=[p_path])

    def _create_project_or_run(self, path, type="project", parents=[],
                               children=[]):
        os.mkdir(path)
        if type == "project":
            self.project_paths.append(path)

        node = {"path": path,
                "type": type,
                "name": os.path.basename(path),
                "children": children,
                "parents": parents}
        nodes.add(self.node_list, node)
