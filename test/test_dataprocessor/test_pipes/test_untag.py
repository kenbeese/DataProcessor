# coding: utf-8

import os
import sys

from ..utility import TestNodeListAndDir

sys.path = [sys.path[0]] \
    + [os.path.join(os.path.dirname(__file__), "../../../lib")] \
    + sys.path[1:]
from dataprocessor.pipes.untag import untag
from dataprocessor.exception import DataProcessorError
import dataprocessor.nodes as nodes
sys.path = [sys.path[0]] + sys.path[2:]


class TestUntag(TestNodeListAndDir):

    def test_untag(self):
        path = os.path.join(self.tempdir_path, "p1/run00")
        tag_path = os.path.join(self.tempdir_path, "p1")

        untag(self.node_list, path, tag_path)

        node = nodes.get(self.node_list, path)
        self.assertFalse(tag_path in node["parents"])
        node = nodes.get(self.node_list, tag_path)
        self.assertFalse(path in node["children"])

    def test_no_path(self):
        path = os.path.join(self.tempdir_path, "p1/nopath")
        tag_path = os.path.join(self.tempdir_path, "p1")

        with self.assertRaisesRegexp(DataProcessorError,
                                     'The path .* of node is not registered.'):
            untag(self.node_list, path, tag_path)

        path = os.path.join(self.tempdir_path, "p1/run01")
        tag_path = os.path.join(self.tempdir_path, "noproject")
        with self.assertRaisesRegexp(DataProcessorError,
                                     'Directory .* does not exist'):
            untag(self.node_list, path, tag_path)

    def test_no_tag(self):
        path = os.path.join(self.tempdir_path, "p1/run01")
        tag_path = os.path.join(self.tempdir_path, "p2")
        with self.assertRaisesRegexp(DataProcessorError,
                                     'The tag .* is not specified.'):
            untag(self.node_list, path, tag_path)
