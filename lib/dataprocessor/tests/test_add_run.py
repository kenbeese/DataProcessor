# coding: utf-8


import os
import sys

from ..utility import TestNodeListAndDir

sys.path = [sys.path[0]] \
    + [os.path.join(os.path.dirname(__file__), "../../../lib")] \
    + sys.path[1:]
from dataprocessor.pipes.add_run import add_run
import dataprocessor.nodes as nodes
sys.path = [sys.path[0]] + sys.path[2:]


class TestAddRun(TestNodeListAndDir):

    def test_add_run_normal(self):
        path = os.path.join(self.tempdir_path, "p1/newrun")
        os.mkdir(path)
        self.node_list = add_run(self.node_list, path)
        self.assertTrue(nodes.get(self.node_list, path))

    def test_add_run_with_kwds(self):
        path = os.path.join(self.tempdir_path, "p1/newrun")
        project_path = os.path.join(self.tempdir_path, "p2")
        os.mkdir(path)
        self.node_list = add_run(self.node_list, path, tag=project_path,
                                 name="foo", comment="foobar")
        node = nodes.get(self.node_list, path)
        self.assertTrue(project_path in node["parents"])
        self.assertEqual("foo", node["name"])
        self.assertEqual("foobar", node["comment"])
