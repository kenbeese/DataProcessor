# -*- coding: utf-8 -*-

from . import helper
from .. import runner

import os.path as op


class TestRunner(helper.TestEnvironment):

    def test_sync(self):
        runner.sync(["true"], self.tempdir_path)
        with self.assertRaises(runner.DataProcessorRunnerError):
            runner.sync(["false"], self.tempdir_path)

    def test_sync_except(self):
        args = ["false", "aa", "bb"]
        try:
            runner.sync(args, self.tempdir_path)
        except runner.DataProcessorRunnerError as e:
            self.assertEqual(e.arguments, args)
            self.assertEqual(e.work_dir, self.tempdir_path)
            self.assertEqual(e.runner, "sync")

    def test_chdir(self):
        runner.sync(["touch", "homhom"], self.tempdir_path)
        self.assertTrue(op.exists(op.join(self.tempdir_path, "homhom")))
