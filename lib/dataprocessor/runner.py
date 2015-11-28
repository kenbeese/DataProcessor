# -*- coding: utf-8 -*-

from . import utility
from .exception import DataProcessorError

import tempfile
import functools
from logging import getLogger, DEBUG
logger = getLogger(__name__)
logger.setLevel(DEBUG)


class DataProcessorRunnerError(DataProcessorError):

    """ Exception about starting run """

    def __init__(self, runner, args, work_dir, exception):
        msg = "runner {} failed. args={}, work_dir={}".format(runner, args, work_dir)
        DataProcessorError.__init__(self, msg)
        self.runner = runner
        self.arguments = args
        self.work_dir = work_dir
        self.exception = exception


runners = {}


def runner(func):
    @functools.wraps(func)
    def wrapper(args, work_dir):
        try:
            func(args, work_dir)
        except Exception as e:
            logger.error(str(e))
            raise DataProcessorRunnerError(func.__name__, args, work_dir, e)
    runners[func.__name__] = wrapper
    return wrapper


@runner
def sync(args, work_dir):
    """ execute command in localhost """
    with utility.chdir(work_dir):
        utility.check_call(args)


@runner
def atnow(args, work_dir):
    atnow_template = """#!/bin/sh
    cd {path}
    {args}
    """
    tmp = tempfile.NamedTemporaryFile()
    tmp.write(atnow_template.format(path=work_dir, args=" ".join(args)))
    tmp.flush()
    utility.check_call(['at', 'now', '-f', tmp.name])


@runner
def systemd_user(args, work_dir):
    """ execute command using systemd-run --user command """
    utility.check_call(["systemd-run", "--user", "-p",
                        "WorkingDirectory={}".format(work_dir)] + args)
