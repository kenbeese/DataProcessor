# coding: utf-8

import os.path
import os
import jinja2
import tempfile
import unittest
import shutil
from .. import utility
from .. import rc

_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "testdata/templates")
_ROOTDIR = os.path.join(os.path.dirname(__file__), "testdata/root")


def _create_environment(temppath):
    _create_ini(temppath)
    _create_nodelist(temppath)
    shutil.copytree(_ROOTDIR, os.path.join(temppath, "root"))


def _create_nodelist(tempdir):
    tempdir = utility.path_expand(tempdir)
    with open(os.path.join(_TEMPLATE_DIR, "data.json")) as f:
        template = jinja2.Template(f.read())

    with open(os.path.join(tempdir, "data.json"), "w") as f:
        f.write(template.render(TEMPORARY_DIRECTORY=tempdir))


def _create_ini(tempdir):
    tempdir = utility.path_expand(tempdir)
    rc.create_configure_file(os.path.join(tempdir, "test.ini"),
                             os.path.join(tempdir, "root"),
                             os.path.join(tempdir, "data.json"),)


def _remove_environment(temppath):
    shutil.rmtree(temppath)


def cli_create():
    tempdir = tempfile.mkdtemp()
    os.putenv("DP_DEBUG_RCPATH", "{}/test.ini".format(tempdir))
    os.putenv("DP_DEBUG_DIR", "{}".format(tempdir))
    _create_environment(tempdir)
    print("Start test environment created in {}.".format(tempdir))
    print(
        "Environment variables DP_DEBUG_RCPATH and DP_DEBUG_DIR are set.")

    try:
        os.system(os.environ["SHELL"])
    finally:
        _remove_environment(tempdir)


class TestEnvironment(unittest.TestCase):

    """
    Create node_list, files, directories and configure file for test.

    Templates of nodelist and configure files exist
    in 'tests/testdata/templates'. Files and Directories exist
    in 'tests/testdata/root'

    Attributes
    ----------
    tempdir_path : str
        path for temporary test environment.
    node_list : list

    """

    def setUp(self):
        self.tempdir_path = tempfile.mkdtemp()
        _create_environment(self.tempdir_path)
        rc.default_rcpath = os.path.join(self.tempdir_path, "test.ini")
        self.node_list = rc.load()

    def tearDown(self):
        _remove_environment(self.tempdir_path)
