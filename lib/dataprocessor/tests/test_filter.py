# coding: utf-8

import os
import unittest

from .utils import TestNodeListAndDir
from .. import filter as dpfilter
from ..nodes import get


class TestFilter(TestNodeListAndDir):

    def test_project(self):
        p_path = self.project_paths[0]
        run_num = len(get(self.node_list, p_path)["children"])
        results = dpfilter.project(self.node_list, p_path)
        for i in xrange(run_num):
            path = os.path.join(p_path, "run%02d" % i)
            self.assertIsNotNone(get(results, path))

    def test_projects(self):
        results = dpfilter.project(self.node_list, self.project_paths)

        run_paths = []
        for p_path in self.project_paths:
            run_paths = run_paths + get(self.node_list, p_path)["children"]

        for run_path in run_paths:
            self.assertIsNotNone(get(results, run_path))

        self.assertEqual(len(results), len(run_paths))

    def test_node_type_project(self):
        results = dpfilter.node_type(self.node_list, "project")
        for path in self.project_paths:
            self.assertIsNotNone(get(results, path))

        self.assertEqual(len(results), len(self.project_paths))

    def test_node_type_run(self):
        results = dpfilter.node_type(self.node_list, "run")

        run_paths = []
        for p_path in self.project_paths:
            run_paths = run_paths + get(self.node_list, p_path)["children"]

        for run_path in run_paths:
            self.assertIsNotNone(get(results, run_path))

        self.assertEqual(len(results), len(run_paths))


class TestPrefixPath(unittest.TestCase):

    def setUp(self):
        self.node_list = [
            {"path": "/foo/bar", "parents": [],
             "children": [],
             "type": "run"},
            {"path": "/foo/bar/foo", "parents": [],
             "children": [],
             "type": "project"},
            {"path": "/foo/barfoo/FOO", "parents": [],
             "children": [],
             "type": "run"},
            {"path": "/bar/foo/bar/FOO", "parents": [],
             "children": [],
             "type": "run"},
        ]

    def test1(self):
        result = dpfilter.prefix_path(self.node_list, "/foo/bar")
        self.assertEqual(len(result), 2)

    def test2(self):
        result = dpfilter.prefix_path(self.node_list, "/foo/bar/")
        self.assertEqual(len(result), 2)

    def test3(self):
        result = dpfilter.prefix_path(self.node_list, "/foo/")
        self.assertEqual(len(result), 3)

    def test4(self):
        result = dpfilter.prefix_path(self.node_list, "foo")
        self.assertEqual(len(result), 0)
