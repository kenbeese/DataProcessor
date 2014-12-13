# coding: utf-8


import os.path
import sys

from ..utility import TestNodeListAndDir

sys.path = [sys.path[0]] \
    + [os.path.join(os.path.dirname(__file__), "../../../lib")] \
    + sys.path[1:]
from dataprocessor.pipes.add_conf import add_conf
import dataprocessor.nodes as nodes
sys.path = [sys.path[0]] + sys.path[2:]


class TestAddConf(TestNodeListAndDir):

    def test_add_conf(self):
        path = os.path.join(self.tempdir_path, "p1/run00")
        self.node_list = add_conf(self.node_list,
                                  path, "foo", "bar")
        self.assertEqual(
            nodes.get(self.node_list, path)["configure"]["foo"], "bar")
