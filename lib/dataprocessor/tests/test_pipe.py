# coding=utf-8

from utils import TestNodeListAndDir

from .. import pipe
from ..exception import DataProcessorError as dpError


@pipe.wrap
def wrap_noreturn(node):
    pass


@pipe.wrap
def wrap_noraise(node):
    raise dpError("will be catched")


@pipe.wrap
def wrap_raise(node):
    raise RuntimeError("cannot catch")


@pipe.file
def file_pipe(node):
    return node


class TestPipe(TestNodeListAndDir):

    def test_noreturn(self):
        with self.assertRaises(pipe.PipeImplementationError):
            wrap_noreturn(self.node_list)

    def test_raise(self):
        nl = wrap_noraise(self.node_list)  # no raise
        self.assertEquals(nl, self.node_list)
        with self.assertRaises(RuntimeError):
            wrap_raise(self.node_list)

    def test_nofilter(self):
        """
        Do not filter node_list.
        """
        nl = file_pipe(self.node_list)
        self.assertEquals(nl, self.node_list)
