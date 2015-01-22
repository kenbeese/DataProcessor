# coding=utf-8

from utils import TestNodeListAndDir

from .. import pipe
from ..exception import DataProcessorError as dpError


@pipe.wrap
def wrap_noreturn(node):
    """Not arrowed"""
    pass


@pipe.wrap
def wrap_noraise(node):
    raise dpError("will be catched")


@pipe.wrap
def wrap_raise(node):
    raise RuntimeError("cannot catch")


class TestPipe(TestNodeListAndDir):

    def test_noreturn(self):
        with self.assertRaises(pipe.PipeImplementError):
            wrap_noreturn(self.node_list)

    def test_raise(self):
        nl = wrap_noraise(self.node_list)  # no raise
        self.assertEquals(nl, self.node_list)
        with self.assertRaises(RuntimeError):
            wrap_raise(self.node_list)
