# coding: utf-8
"""Test for add_node."""
import os
import copy

from .utils import TestNodeListAndDir
from ..pipes.add_node import add_node
from .. import nodes


class TestAddNode(TestNodeListAndDir):

    def test_add_node(self):
        compare_list = self._create_compare_node_list()

        runpath = os.path.join(self.project_paths[0], "run02")
        add_node(self.node_list, path=runpath, parents=self.project_paths[0],
                 strategy="modest_update")
        self.assertEqual(self.node_list, compare_list)

    def _create_compare_node_list(self):
        compare_list = copy.deepcopy(self.node_list)
        for n in self.node_list:
            nodes.validate_link(self.node_list, n)
        node = {
            "path": os.path.join(self.project_paths[0], "run02"),
            "parents": [self.project_paths[0]],
            "children": []
        }
        nodes.add(compare_list, node, strategy="modest_update")
        return compare_list
