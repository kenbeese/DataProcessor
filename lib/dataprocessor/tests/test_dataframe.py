# coding=utf-8
import unittest
from pandas import DataFrame

from .. import dataframe
from ..exception import DataProcessorError as dpError


class TestIo(unittest.TestCase):

    """Unittest for dataprocessor.dataframe.

    Attributes
    ----------
    node_list : list
        list of project root dir path

    """

    def setUp(self):
        self.children = ["/proj1/0", "/proj1/1", "/proj1/2"]
        self.node_list = [
            {"path": "/proj1", "parents": [], "name": "proj1",
             "children": self.children, "type": "project"},
            {"path": "/proj1/0", "parents": ["/proj1"],
             "children": [], "type": "run", "name": "0",
             "configure": {"A": 1.0, "B": 2, "C": "homhom"}},
            {"path": "/proj1/1", "parents": ["/proj1"],
             "children": [], "type": "run", "name": "1",
             "configure": {"A": 2.0, "B": 3, "C": "madoka"}},
            {"path": "/proj1/2", "parents": ["/proj1"],
             "children": [], "type": "run", "name": "2",
             "configure": {"A": 3.0, "D": u"私って本当バカ"}}
        ]
        col = set([])
        for n in self.node_list:
            if "configure" not in n:
                continue
            for c in n["configure"]:
                col.add(c)
        self.configures = col

    def test_get_projects(self):
        projects = dataframe.get_projects(self.node_list)
        projects_m = DataFrame([{
            "name": "proj1",
            "path": "/proj1",
            "children": self.children,
            "type": "project",
            "parents": [],
        }])
        self.assertTrue(projects.equals(projects_m))

    def test_get_project(self):
        df = dataframe.get_project(self.node_list, "/proj1")
        self.assertItemsEqual(df.index, self.children)
        col = self.configures
        # default properties
        col.add("name")
        col.add("path")
        # col.add("comment")
        # remove index property
        col.discard("path")
        self.assertItemsEqual(df.columns, col)

    def test_get_project_multi_index(self):
        df = dataframe.get_project(self.node_list, "/proj1", index=["path", "name"])
        col = self.configures
        self.assertItemsEqual(df.columns, col)
        indices = []
        for n in self.node_list:
            if n["type"] is not "run":
                continue
            indices.append((n["path"], n["name"]))
        self.assertItemsEqual(df.index, indices)

    def test_get_project_invalid_inputs(self):
        # invalid project name
        with self.assertRaises(dpError):
            dataframe.get_project(self.node_list, "proj1")
        # invalid index
        with self.assertRaises(dpError):
            dataframe.get_project(self.node_list, "/proj1", index=1)
        with self.assertRaises(dpError):
            dataframe.get_project(self.node_list, "/proj1", index="pat")
        with self.assertRaises(dpError):
            dataframe.get_project(self.node_list, "/proj1", index=["pat", "name"])
        # not raise
        dataframe.get_project(self.node_list, "/proj1", index=[])
