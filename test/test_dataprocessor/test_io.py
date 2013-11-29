# coding=utf-8
import sys
import os
import tempfile
import copy
import unittest

sys.path = [sys.path[0]] \
    + [os.path.join(os.path.dirname(__file__), "../../../lib")] \
    + sys.path[1:]
import dataprocessor.io as io
import dataprocessor.nodes as nodes
sys.path = [sys.path[0]] + sys.path[2:]


class TestIo(unittest.TestCase):

    def setUp(self):
        self.jsonfile = os.path.join(tempfile.mkdtemp(), "dat.json")
        open(self.jsonfile, "a").close()

    def tearDown(self):
        import shutil
        shutil.rmtree(os.path.dirname(self.jsonfile))

    def test_datahandler1(self):
        node_list = [{"path": "/path/to/hogehoge", "name": "Oh"},
                     {"path": "/path/to/2", "name": "Yeah!!",
                      "parents": ["/path/to/foo"], "children": []}]
        added_node = {"path": "/path/to/foo", "name": "yahoooooo",
                      "parents": [], "children": ["/path/to/2"]}
        # Create json file
        io.save(node_list, self.jsonfile, silent=True)

        compare_node_list = copy.deepcopy(node_list)
        nodes.add(compare_node_list, copy.deepcopy(added_node))

        with io.DataHandler(self.jsonfile, True) as data:
            data.add(added_node)
            self.assertEqual(data.get(), compare_node_list)

        node_list = io.load([], self.jsonfile)
        self.assertEqual(node_list, compare_node_list)

    def test_datahandler2(self):
        node_list = [{"path": "/path/to/hogehoge", "name": "Oh"},
                     {"path": "/path/to/2", "name": "Yeah!!"}]
        replace_node_list = [{"path": "/path/to/foo", "name": "yahoooooo"}]
        # Create json file
        io.save(node_list, self.jsonfile, silent=True)

        compare_node_list = copy.deepcopy(replace_node_list)

        with io.DataHandler(self.jsonfile, True) as data:
            data.replace(replace_node_list)

        node_list = io.load([], self.jsonfile)
        self.assertEqual(node_list, compare_node_list)
