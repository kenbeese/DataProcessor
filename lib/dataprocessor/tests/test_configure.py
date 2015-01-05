# coding: utf-8

import os.path as op
import unittest
from ..utility import check_directory
from ..pipes.configure import add, no_section


ROOT = op.join(__file__, "../../../../sample/datadir")

class TestConfigure_INI(unittest.TestCase):

    def setUp(self):
        self.node_list = [{
            "path": check_directory(op.join(ROOT, "project2/run01")),
            "type": "run",
        }]

    def test_add(self):
        nl = add(self.node_list, "parameters.ini")
        self.assertEqual(nl[0]["configure"], {"ny": "23"})
        nl = add(nl, "parameters.ini")  # 二回しても大丈夫
        self.assertEqual(nl[0]["configure"], {"ny": "23"})

    def test_add_filetype(self):
        nl = add(self.node_list, "parameters.ini", filetype="yaml")
        self.assertNotIn("configure", nl[0])  # fail to parse YAML
        nl = add(self.node_list, "parameters.ini", filetype="INI")
        self.assertEqual(nl[0]["configure"], {"ny": "23"})

    def test_add_missing_name(self):
        add(self.node_list, "parame.yamlu")  # not raises


class TestConfigure_YAML(unittest.TestCase):

    def setUp(self):
        self.node_list = [{
            "path": check_directory(op.join(ROOT, "project3/run01")),
            "type": "run",
        }]

    def test_add(self):
        nl = add(self.node_list, "parameters.yml")
        self.assertEqual(nl[0]["configure"], {"ny": 23})
        nl = add(nl, "parameters.yml")
        self.assertEqual(nl[0]["configure"], {"ny": 23})

    def test_add_filetype_yaml(self):
        nl = add(self.node_list, "parameters.yml", filetype="INI")
        self.assertNotIn("configure", nl[0])  # fail to parse YAML
        nl = add(self.node_list, "parameters.yml", filetype="YAML")
        self.assertEqual(nl[0]["configure"], {"ny": 23})


class TestConfigure_CONF(unittest.TestCase):

    def setUp(self):
        self.node_list = [{
            "path": check_directory(op.join(ROOT, "project1/run01")),
            "type": "run",
        }]

    def test_add_conf(self):
        nl = add(self.node_list, "parameters.conf")
        self.assertEqual(nl[0]["configure"]["nx"], "12")
        self.assertEqual(nl[0]["configure"]["ny"], "32")
