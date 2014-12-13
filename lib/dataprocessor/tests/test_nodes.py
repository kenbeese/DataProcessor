# coding=utf-8
"""Test for nodes."""
import os
import unittest
import copy

from .utils import TestNodeListAndDir
from .. import nodes


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

    def test_add_update_skip_validate_link(self):
        node_list = copy.deepcopy(self.node_list)
        new_node = {
            "path": "/path/0",
            "parents": ["/path/2"],
            "children": ["/path/1", "/path/3"]
        }
        nodes.add(node_list, new_node, skip_validate_link=True)

        compare_node_list = [
            {"path": "/path/0", "parents": ["/path/2"],
             "children": ["/path/1", "/path/3"]},  # updated
            {"path": "/path/1", "parents": [],
             "children": ["/path/0"]},
            {"path": "/path/2", "parents": ["/path/0"],
             "children": []},
            {"path": "/path/3", "parents": ["/path/0"],
             "children": []}]
        self.assertEqual(node_list, compare_node_list)

    def test_add_update_validate_link(self):
        node_list = copy.deepcopy(self.node_list)
        new_node = {
            "path": "/path/1",
            "parents": ["/path/0"],
            "children": []
        }
        nodes.add(node_list, new_node)

        compare_node_list = [
            {"path": "/path/0", "parents": ["/path/1"],
             "children": ["/path/2", "/path/3", "/path/1"]},
            {"path": "/path/1", "parents": ["/path/0"],
             "children": []},
            {"path": "/path/2", "parents": ["/path/0"],
             "children": []},
            {"path": "/path/3", "parents": ["/path/0"],
             "children": []}]
        self.assertEqual(node_list, compare_node_list)

    def test_add_replace_skip_validate_link(self):
        node_list = copy.deepcopy(self.node_list)
        node_list[0]["comment"] = "madoka"
        new_node = copy.deepcopy(self.node_list[0])
        nodes.add(node_list, new_node, skip_validate_link=True,
                  strategy="replace")

        compare_node_list = [
            {"path": "/path/1", "parents": [],
             "children": ["/path/0"]},
            {"path": "/path/2", "parents": ["/path/0"],
             "children": []},
            {"path": "/path/3", "parents": ["/path/0"],
             "children": []},
            {"path": "/path/0", "parents": ["/path/1"],
             "children": ["/path/2", "/path/3"]},
        ]
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
            {"path": "/path/3", "parents": ["/path/0"], "children": [], }]
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

    def test_merge_duplicate(self):
        node_list = [
            {"path": "/path/0", "parents": ["/path/1"],
             "children": ["/path/2", "/path/3"]},
            {"path": "/path/1", "parents": [],
             "children": ["/path/0"]},
            {"path": "/path/2", "parents": ["/path/0"],
             "children": []},
            {"path": "/path/3", "parents": ["/path/0"],
             "children": [], "attr1": "value1"},
            {"path": "/path/3", "parents": ["/path/0"],
             "children": [], "attr1": "value2"}  # duplicated
        ]
        node_list_ans = [
            {"path": "/path/0", "parents": ["/path/1"],
             "children": ["/path/2", "/path/3"]},
            {"path": "/path/1", "parents": [],
             "children": ["/path/0"]},
            {"path": "/path/2", "parents": ["/path/0"],
             "children": []},
            {"path": "/path/3", "parents": ["/path/0"],
             "children": [], "attr1": "value2"}  # updated by later one
        ]

        node_list = nodes.merge_duplicate(node_list)
        self.assertEqual(node_list, node_list_ans)


class TestChangePath(TestNodeListAndDir):

    def test_change_path_having_children(self):
        after_path = os.path.join(self.project_paths[0], "moved_dir")
        before_path = self.project_paths[0]
        os.mkdir(after_path)
        nodes.change_path(
            self.node_list, before_path, after_path, silent=True)

        changed_node = nodes.get(self.node_list, after_path)
        # check target node path
        self.assertIsNotNone(changed_node)

        # check children node path
        for p in changed_node["children"]:
            child_node = nodes.get(self.node_list, p)
            self.assertIn(after_path, child_node["parents"])
            self.assertNotIn(before_path, child_node["parents"])

    def test_change_path_having_parents(self):
        after_path = os.path.join(self.project_paths[0], "moved_dir")
        before_path = os.path.join(self.project_paths[0], "run01")
        os.mkdir(after_path)
        nodes.change_path(
            self.node_list, before_path, after_path, silent=True)

        # check path
        self.assertIsNotNone(nodes.get(self.node_list, after_path))

        # check parents path
        project_node = nodes.get(self.node_list, self.project_paths[0])
        self.assertIn(after_path, project_node["children"])
        self.assertNotIn(before_path, project_node["children"])
