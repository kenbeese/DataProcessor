# coding=utf-8

import os.path as op
import unittest
from ..utility import abspath
from ..pipes.remove_dead import remove_dead

ROOT = op.join(__file__, "../../../../sample/datadir")

class TestRemoveDead(unittest.TestCase):

    def setUp(self):
        # second one does not exist
        self.node_list = [{
            "path": abspath(op.join(ROOT, "project2/run01")),
            "type": "run",
            "parents": [],
            "children": [],
        }, {
            "path": abspath(op.join(ROOT, "project2/dead")),
            "type": "run",
            "parents": [],
            "children": [],
        }]

    def testRemoveDead(self):
        node_list = remove_dead(self.node_list)
        self.assertEqual(len(node_list), 1)
        self.assertEqual(node_list[0]["path"],
                         abspath(op.join(ROOT, "project2/run01")))
