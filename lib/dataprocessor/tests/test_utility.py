import os
import unittest
import tempfile

from .. import utility
from ..exception import DataProcessorError


class TestUtility(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tempdir)

    def test_check_file(self):
        tempfile = os.path.join(self.tempdir, "foo")
        with self.assertRaises(DataProcessorError):
            utility.check_file(tempfile)
        open(tempfile, "a").close()
        utility.check_file(tempfile)  # not raise

        dir_path = os.path.join(self.tempdir, "bar")
        with self.assertRaises(DataProcessorError):
            utility.check_file(dir_path)
        os.mkdir(dir_path)
        with self.assertRaises(DataProcessorError):
            utility.check_file(dir_path)

    def test_check_dir(self):
        tempfile = os.path.join(self.tempdir, "foo")
        with self.assertRaises(DataProcessorError):
            utility.check_dir(tempfile)
        open(tempfile, "a").close()
        with self.assertRaises(DataProcessorError):
            utility.check_dir(tempfile)

        dir_path = os.path.join(self.tempdir, "bar")
        with self.assertRaises(DataProcessorError):
            utility.check_dir(dir_path)
        os.mkdir(dir_path)
        utility.check_dir(dir_path)  # not raise

    def test_check_or_create(self):
        tempfile = os.path.join(self.tempdir, "foo")
        open(tempfile, "a").close()
        with self.assertRaises(DataProcessorError):
            utility.check_or_create_dir(tempfile)

        temp_dir = os.path.join(self.tempdir, "bar")
        self.assertFalse(os.path.exists(temp_dir))
        utility.check_or_create_dir(temp_dir)  # not raise, create
        self.assertTrue(os.path.exists(temp_dir))
        utility.check_or_create_dir(temp_dir)  # not raise
