# coding: utf-8


import os.path

from .utils import TestNodeListAndDir

from ..pipes.add_conf import add_conf
from .. import nodes


class TestAddConf(TestNodeListAndDir):

    def test_add_conf(self):
        path = os.path.join(self.tempdir_path, "p1/run00")
        self.node_list = add_conf(self.node_list,
                                  path, "foo", "bar")
        self.assertEqual(
            nodes.get(self.node_list, path)["configure"]["foo"], "bar")
