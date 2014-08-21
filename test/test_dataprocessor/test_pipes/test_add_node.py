# coding: utf-8
"""Test for add_node."""
import os
import sys
import copy


from ..utility import TestNodeListAndDir

sys.path = [sys.path[0]] \
    + [os.path.join(os.path.dirname(__file__), "../../../lib")] \
    + sys.path[1:]
from dataprocessor.pipes.add_node import add_node
import dataprocessor.nodes as nodes
sys.path = [sys.path[0]] + sys.path[2:]


class TestAddNode(TestNodeListAndDir):

    def test_add_node(self):
        compare_list = self._create_compare_node_list()

        runpath = os.path.join(self.tempdir_paths[0], "run02")
        add_node(self.node_list, path=runpath, parents=self.tempdir_paths[0])
        self.assertEqual(self.node_list, compare_list)

    def _create_compare_node_list(self):
        compare_list = copy.deepcopy(self.node_list)
        for n in self.node_list:
            nodes.validate_link(self.node_list, n)
        node = {"path": os.path.join(self.tempdir_paths[0], "run02"),
                "parents": [self.tempdir_paths[0]]}
        nodes.add(compare_list, node)
        return compare_list
