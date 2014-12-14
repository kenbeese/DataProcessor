# coding=utf-8
import unittest
from .. import pipes


class TestPipes(unittest.TestCase):

    def setUp(self):
        self.pipes_dics = {
            "foo": {
                "func": "foo",
                "args": [("bar", {"help": "baarrr"})],
                "kwds": [("BAR", {"help": "barRRRR"})],
                "desc": "FFFFOOR"
            },
        }

    def test_validate(self):
        self.assertIsNone(pipes._validate_pipes(self.pipes_dics))

    def test_validate_fail1(self):
        self.pipes_dics["bar"] = {
            "func": "bar",
            "args": ["ffff", "fooo"],
            "kwds": [("bar", {"help": "bar"})],
            "desc": "bbbbbarrr"
        }
        with self.assertRaises(pipes.InvalidPipeError):
            pipes._validate_pipes(self.pipes_dics)

    def test_validate_fail2(self):
        self.pipes_dics["bar"] = {
            "func": "bar",
            "args": [("ffff", {"help": "ffffff"}),
                     ("fooo", {"help": "fooooooooo"})],
            "kwds": ["bar"],
            "desc": "bbbbbarrr"
        }
        with self.assertRaises(pipes.InvalidPipeError):
            pipes._validate_pipes(self.pipes_dics)

    def test_convert_old_pipes_dics(self):
        self.pipes_dics["bar"] = {
            "func": "bar",
            "args": ["ffff", "fooo"],
            "kwds": ["bar"],
            "desc": "bbbbbarrr"
        }
        valid_dic = {
            "func": "bar",
            "args": [("ffff", {"help": "ffff"}),
                     ("fooo", {"help": "fooo"})],
            "kwds": [("bar", {"help": "bar"})],
            "desc": "bbbbbarrr"
        }

        pipes._convert_old_pipes_dics(self.pipes_dics)
        self.assertEqual(self.pipes_dics["bar"], valid_dic)

    def test_convert_old_pipes_dics_fail(self):
        self.pipes_dics["bar"] = {
            "func": "bar",
            "args": ["ffff", ("fooo", {"help": "FOOO"})],
            "kwds": ["bar"],
            "desc": "bbbbbarrr"
        }
        valid_dic = {
            "func": "bar",
            "args": [("ffff", {"help": "ffff"}),
                     ("fooo", {"help": "FOOO"})],
            "kwds": [("bar", {"help": "bar"})],
            "desc": "bbbbbarrr"
        }

        pipes._convert_old_pipes_dics(self.pipes_dics)
        self.assertNotEqual(self.pipes_dics["bar"], valid_dic)
