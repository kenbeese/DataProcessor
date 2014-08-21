# coding: utf-8

import os
import sys
import unittest

sys.path = [sys.path[0]] \
    + [os.path.join(os.path.dirname(__file__), "../../../lib")] \
    + sys.path[1:]
import dataprocessor as dp
sys.path = [sys.path[0]] + sys.path[2:]


class TestNodes(unittest.TestCase):

    """Unittest for dataprocessor.filter.

    Attributes
    ----------
    node_list : list
        list of project root dir path

    """

    def setUp(self):
        self.node_list = [
            {"path": "/path/0", "parents": ["/path/1"],
             "children": [],
             "type": "run"},
            {"path": "/path/1", "parents": [],
             "children": ["/path/0", "/path/2"],
             "type":"project"},
            {"path": "/path/2", "parents": ["/path/1"],
             "children": [],
             "type": "run"},
            {"path": "/path/3", "parents": ["/path/4"],
             "children": [],
             "type": "run"},
            {"path": "/path/4", "parents": [],
             "children": ["/path/3"],
             "type":"project"}, ]

    def test_project(self):
        result = dp.filter.project(self.node_list, "/path/1")
        runs = [{'path': '/path/0',
                 'parents': ['/path/1'],
                 'children': [],
                 'type': 'run'},
                {'path': '/path/2',
                 'parents': ['/path/1'],
                 'children': [],
                 'type': 'run'}]
        self.assertEqual(result, runs)

    def test_node_type(self):
        result = dp.filter.node_type(self.node_list, "project")
        projects = [{'path': '/path/1',
                     'parents': [],
                     'children': ['/path/0', '/path/2'],
                     'type': 'project'},
                    {'path': '/path/4',
                     'parents': [],
                     'children': ['/path/3'],
                     'type': 'project'}]
        self.assertEqual(result, projects)

        result = dp.filter.node_type(self.node_list, "run")
        runs = [{'path': '/path/0',
                 'parents': ['/path/1'],
                 'children': [],
                 'type': 'run'},
                {'path': '/path/2',
                 'parents': ['/path/1'],
                 'children': [],
                 'type': 'run'},
                {'path': '/path/3',
                 'parents': ['/path/4'],
                 'children': [],
                 'type': 'run'}]
        self.assertEqual(result, runs)
