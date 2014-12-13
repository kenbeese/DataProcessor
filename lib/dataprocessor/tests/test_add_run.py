# coding: utf-8


import os

from .utils import TestNodeListAndDir
from ..pipes.add_run import add_run
from .. import nodes


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
