# coding=utf-8
import unittest
from pandas import DataFrame

from .. import dataframe as df


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

    def test_get_projects(self):
        projects = df.get_projects(self.node_list)
        projects_m = DataFrame([{
            "name": "proj1",
            "path": "/proj1",
            "children": self.children,
            "type": "project",
            "parents": [],
        }])
        self.assertTrue(projects.equals(projects_m))
