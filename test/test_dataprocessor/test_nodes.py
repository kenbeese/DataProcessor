# coding=utf-8
"""Test for nodes."""
import os
import sys
import unittest
import copy

sys.path = [sys.path[0]] \
    + [os.path.join(os.path.dirname(__file__), "../../../lib")] \
    + sys.path[1:]
import dataprocessor.nodes as nodes
sys.path = [sys.path[0]] + sys.path[2:]


class TestNodes(unittest.TestCase):

    """Unittest for dataprocessor.nodes.

    Attributes
    ----------
    node_list : list
        list of project root dir path

    """

    def setUp(self):
        self.node_list = [
            {"path": "/path/0", "parents": ["/path/1"],
             "children": ["/path/2", "/path/3"]},
            {"path": "/path/1", "parents": [],
             "children": ["/path/0"]},
            {"path": "/path/2", "parents": ["/path/0"],
             "children": []},
            {"path": "/path/3", "parents": ["/path/0"],
             "children": []}]

    def test_add_skip_validate_link(self):
        node_list = copy.deepcopy(self.node_list)
        added_node = {"path": "/added/path", "parents": ["/path/2"],
                      "children": []}
        nodes.add(node_list, added_node, skip_validate_link=True)

        compare_node_list = [
            {"path": "/path/0", "parents": ["/path/1"],
             "children": ["/path/2", "/path/3"]},
            {"path": "/path/1", "parents": [], "children": ["/path/0"]},
            {"path": "/path/2", "parents": ["/path/0"], "children": []},
            {"path": "/path/3", "parents": ["/path/0"], "children": []},
            {"path": "/added/path", "parents": ["/path/2"], "children": []}]
        self.assertEqual(node_list, compare_node_list)

    def test_add_validate_link1(self):
        node_list = copy.deepcopy(self.node_list)
        added_node = {"path": "/added/path", "parents": ["/path/2"],
                      "children": []}
        nodes.add(node_list, added_node)

        compare_node_list = [
            {"path": "/path/0", "parents": ["/path/1"],
             "children": ["/path/2", "/path/3"]},
            {"path": "/path/1", "parents": [], "children": ["/path/0"]},
            {"path": "/path/2", "parents": ["/path/0"],
             "children": ["/added/path"]},
            {"path": "/path/3", "parents": ["/path/0"], "children": []},
            {"path": "/added/path", "parents": ["/path/2"], "children": []}]
        self.assertEqual(node_list, compare_node_list)

    def test_add_validate_link2(self):
        node_list = copy.deepcopy(self.node_list)
        added_node = {"path": "/added/path", "parents": [],
                      "children": ["/path/3"]}
        nodes.add(node_list, added_node)

        compare_node_list = [
            {"path": "/path/0", "parents": ["/path/1"],
             "children": ["/path/2", "/path/3"]},
            {"path": "/path/1", "parents": [], "children": ["/path/0"]},
            {"path": "/path/2", "parents": ["/path/0"],
             "children": []},
            {"path": "/path/3", "parents": ["/path/0", "/added/path"],
             "children": []},
            {"path": "/added/path", "parents": [], "children": ["/path/3"]}]
        self.assertEqual(node_list, compare_node_list)

    def test_remove_skip_validate_link(self):
        node_list = copy.deepcopy(self.node_list)
        nodes.remove(node_list, "/path/0", skip_validate_link=True)
        compare_node_list = [
            {"path": "/path/1", "parents": [], "children": ["/path/0"]},
            {"path": "/path/2", "parents": ["/path/0"], "children": []},
            {"path": "/path/3", "parents": ["/path/0"], "children": []}]
        self.assertEqual(node_list, compare_node_list)

    def test_remove_validate_link1(self):
        node_list = copy.deepcopy(self.node_list)
        nodes.remove(node_list, "/path/0")
        # This state is OK? These node are not related to some node.
        # Such node is allowed only when the node type is project.
        compare_node_list = [
            {"path": "/path/1", "parents": [], "children": []},
            {"path": "/path/2", "parents": [], "children": []},
            {"path": "/path/3", "parents": [], "children": []}]
        self.assertEqual(node_list, compare_node_list)

    def test_remove_validate_link2(self):
        node_list = copy.deepcopy(self.node_list)
        nodes.remove(node_list, "/path/1")
        compare_node_list = [
            {"path": "/path/0", "parents": [], "children": ["/path/2",
                                                            "/path/3"]},
            {"path": "/path/2", "parents": ["/path/0"], "children": []},
            {"path": "/path/3", "parents": ["/path/0"], "children": []}]
        self.assertEqual(node_list, compare_node_list)

    def test_remove_validate_link3(self):
        node_list = copy.deepcopy(self.node_list)
        nodes.remove(node_list, "/path/3")
        compare_node_list = [
            {"path": "/path/0",
             "parents": ["/path/1"], "children": ["/path/2"]},
            {"path": "/path/1", "parents": [], "children": ["/path/0"]},
            {"path": "/path/2", "parents": ["/path/0"], "children": []}]
        self.assertEqual(node_list, compare_node_list)

    def test_validate_link_complete(self):
        node_list = [
            {"path": "/path/0", "parents": ["/path/1"],
             "children": ["/path/2"]},                      # incomplete
            {"path": "/path/1", "parents": [], "children": ["/path/0"]},
            {"path": "/path/2", "parents": [],              # incomplete
             "children": []},
            {"path": "/path/3", "parents": ["/path/0"], "children": [],}]
        # complete /path/2
        nodes.validate_link(node_list, node_list[0])
        # complete /path/0
        nodes.validate_link(node_list, node_list[3])
        self.assertEqual(node_list, self.node_list)

    def test_validate_link_remove(self):
        node_list = [
            {"path": "/path/0",
             "parents": ["/path/1", "/not/exists2"],  # does not exist
             "children": ["/path/2", "/path/3"]},
            {"path": "/path/1", "parents": [], "children": ["/path/0"]},
            {"path": "/path/2", "parents": ["/path/0"], "children": []},
            {"path": "/path/3", "parents": ["/path/0"],
             "children": ["/not/exists"],                    # does not exist
             }]
        # remove not exist parents link
        nodes.validate_link(node_list, node_list[0], True)
        # remove not exist children link
        nodes.validate_link(node_list, node_list[3], True)
        self.assertEqual(node_list, self.node_list)
