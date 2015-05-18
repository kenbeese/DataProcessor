# coding: utf-8

import os

from .utils import TestNodeListAndDir

from ..pipes.untag import untag
from ..exception import DataProcessorError
from .. import nodes


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
                                     'The path .* of project is not registered'):
            untag(self.node_list, path, tag_path)

    def test_no_tag(self):
        path = os.path.join(self.tempdir_path, "p1/run01")
        tag_path = os.path.join(self.tempdir_path, "p2")
        with self.assertRaisesRegexp(DataProcessorError,
                                     'The tag .* is not specified.'):
            untag(self.node_list, path, tag_path)

    def test_untag_itself(self):
        node = self.node_list[0]
        path = node["path"]
        node["children"].append(path)
        node["parents"].append(path)
        untag(self.node_list, path, path)
        self.assertFalse(path in node["children"])
        self.assertFalse(path in node["parents"])
        self.assertTrue(node in self.node_list)
