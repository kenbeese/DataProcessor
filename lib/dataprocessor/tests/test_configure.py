# coding: utf-8

import os.path as op
import unittest
from .helper import TestEnvironment
from ..utility import abspath
from ..pipes.configure import load
from .. import configure
from ..configure import FileType, guess_filetype_from_path

ROOT = op.join(__file__, "../../../../sample/datadir")


class TestFileType(unittest.TestCase):

    def test_get_filetype(self):
        self.assertEqual(FileType.ini,
                         guess_filetype_from_path("/path/to/hoge.ini"))
        self.assertEqual(FileType.ini,
                         guess_filetype_from_path("/path/to/hoge.conf"))
        self.assertEqual(FileType.yaml,
                         guess_filetype_from_path("/path/to/hoge.yml"))
        self.assertEqual(FileType.yaml,
                         guess_filetype_from_path("/path/to/hoge.yaml"))
        self.assertEqual(FileType.NONE,
                         guess_filetype_from_path("/path/to/hoge.jpg"))


class TestConfigure_INI(unittest.TestCase):

    def setUp(self):
        self.node_list = [{
            "path": abspath(op.join(ROOT, "project2/run01")),
            "type": "run",
        }]

    def test_load(self):
        nl = load(self.node_list, "parameters.ini")
        self.assertEqual(nl[0]["configure"], {"ny": "23"})
        nl = load(nl, "parameters.ini")  # works if there already exist "configure"
        self.assertEqual(nl[0]["configure"], {"ny": "23"})

    def test_load_filetype(self):
        nl = load(self.node_list, "parameters.ini", filetype="yaml")
        self.assertNotIn("configure", nl[0])  # fail to parse YAML
        nl = load(self.node_list, "parameters.ini", filetype="INI")
        self.assertEqual(nl[0]["configure"], {"ny": "23"})

    def test_invalid_filetype(self):
        nl = load(self.node_list, "parameters.ini", filetype="ababababa")
        self.assertEqual(nl[0]["configure"], {"ny": "23"})

    def test_load_missing_name(self):
        load(self.node_list, "parame.yamlu")  # not raises


class TestConfigure_YAML(unittest.TestCase):

    def setUp(self):
        self.node_list = [{
            "path": abspath(op.join(ROOT, "project3/run01")),
            "type": "run",
        }]

    def test_load(self):
        nl = load(self.node_list, "parameters.yml")
        self.assertEqual(nl[0]["configure"], {"ny": 23})
        nl = load(nl, "parameters.yml")
        self.assertEqual(nl[0]["configure"], {"ny": 23})

    def test_load_filetype_yaml(self):
        nl = load(self.node_list, "parameters.yml", filetype="INI")
        self.assertNotIn("configure", nl[0])  # fail to parse YAML
        nl = load(self.node_list, "parameters.yml", filetype="YAML")
        self.assertEqual(nl[0]["configure"], {"ny": 23})


class TestConfigure_CONF(unittest.TestCase):

    def setUp(self):
        self.node_list = [{
            "path": abspath(op.join(ROOT, "project1/run01")),
            "type": "run",
        }]

    def test_load_conf(self):
        nl = load(self.node_list, "parameters.conf")
        self.assertEqual(nl[0]["configure"]["nx"], "12")
        self.assertEqual(nl[0]["configure"]["ny"], "32")


class TestConfigure_NoSection(TestEnvironment):

    def test_load_conf(self):
        nl = [{
            "path": abspath(op.join(ROOT, "project4/run01")),
            "type": "run",
        }]
        nl = load(nl, "parameters.cfg", filetype="nosection")
        self.assertEqual(nl[0]["configure"]["N"], "10")
        self.assertEqual(nl[0]["configure"]["A"], "1.0")

    def test_read_configure1(self):
        configure_path = op.join(self.tempdir_path, "conf")
        contents = """hgoe=1\nhoge=2\ndafo=ds\n#hoge=ds"""
        self.create_file(configure_path, contents)
        conf = configure.parse_nosection(configure_path)
        self.assertEqual(conf, {"hgoe": "1", "hoge": "2", "dafo": "ds"})

    def test_read_configure2(self):
        configure_path = op.join(self.tempdir_path, "conf")
        # does not comment.
        contents = """hgoe=1\nhoge=2\ndafo=ds\n #hoge=ds"""
        self.create_file(configure_path, contents)
        conf = configure.parse_nosection(configure_path)
        self.assertEqual(conf, {"hgoe": "1", "hoge": "2",
                                "dafo": "ds", "#hoge": "ds"})

    def test_read_configure3(self):
        configure_path = op.join(self.tempdir_path, "conf")
        contents = """hgoe:1\nhoge   :   2\ndafo : ds\n!hoge=ds"""
        self.create_file(configure_path, contents)
        conf = configure.parse_nosection(configure_path, ":", "!")
        self.assertEqual(conf, {"hgoe": "1", "hoge": "2", "dafo": "ds"})

    def create_file(self, path, contents):
        with open(path, "w") as f:
            f.write(contents)
