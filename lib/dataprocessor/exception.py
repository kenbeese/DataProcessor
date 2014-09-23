# coding=utf-8
import traceback
from contextlib import contextmanager


class DataProcessorError(Exception):

    """A runtime error occurred in DataProcessor

    This exception is raised when invalid manipulation is done.
    This exception will be caught in dataprocessor.execute,
    and converted into InvalidJSONError.

    Attributes
    ----------
    msg : str
        A message for the error

    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class InvalidJSONError(Exception):

    """A runtime error occurred in processing manipulation

    Attributes
    ----------
    name : str
        The name of pipe in which error occurred.
    msg : str
        A message for the error

    """

    def __init__(self, name, msg):
        self.name = name
        self.msg = msg

    def __str__(self):
        return "[%s]: %s" % (self.name, self.msg)


@contextmanager
def pipe_execute(name):
    try:
        yield
    except DataProcessorError as e:
        print(traceback.format_exc())
        raise InvalidJSONError(name, e.msg)
