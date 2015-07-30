# -*- coding: utf-8 -*-

from . import helper
from .. import starter, basket, nodes, utility
from ..exception import DataProcessorError as dpError

import os.path as op


class TestStarter(helper.TestEnvironment):

    def test_start(self):
        N = len(self.node_list)
        node = starter.start(self.node_list, ["touch", "homhom"], [])
        self.assertEqual(len(self.node_list), N + 1)
        path = node["path"]
        self.assertTrue(op.exists(op.join(path, "homhom")))

    def test_start_projects(self):
        N = len(self.node_list)
        node = starter.start(self.node_list, ["touch", "homhom"], [],
                             projects=["mado_magi"])
        self.assertEqual(len(self.node_list), N + 2)
        project_path = basket.get_tag_abspath("mado_magi")
        self.assertTrue(op.exists(project_path))
        self.assertTrue(project_path in node["parents"])

        project_node = nodes.get(self.node_list, project_path)
        self.assertTrue(node["path"] in project_node["children"])

    def test_start_requirements(self):
        fn = "mami.txt"
        comment = "We must die."
        with utility.chdir(self.tempdir_path):
            with open(fn, "w") as f:
                f.write(comment)
            node = starter.start(self.node_list, ["test", "-e", fn], [fn, ])
        path = node["path"]
        self.assertTrue(op.exists(op.join(path, fn)))
        self.assertEqual(open(op.join(path, fn), "r").read(), comment)

    def test_start_name(self):
        name = "sayaka"
        node = starter.start(self.node_list, ["touch", "homhom"], [], name=name)
        path = node["path"]
        self.assertEqual(op.basename(path), name)

        with self.assertRaisesRegexp(dpError, "Already exists: .*"):
            starter.start(self.node_list, ["touch", "homhom"], [], name=name)
