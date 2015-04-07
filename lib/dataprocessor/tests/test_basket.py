# coding: utf-8

from . import helper
from .. import basket
from ..exception import DataProcessorError as dpError

import os
import os.path as op
from contextlib import contextmanager


@contextmanager
def chdir(dirname):
    cwd = os.getcwd()
    os.chdir(dirname)
    yield
    os.chdir(cwd)


class TestBasket(helper.TestEnvironment):

    def test_ready_basket(self):
        run_basket = basket._ready_basket(None, "Runs")
        self.assertEqual(run_basket, op.join(self.tempdir_path, "root/Runs"))
        self.assertTrue(op.exists(run_basket))

    def test_resolve_project_path_name(self):
        p_path = basket.resolve_project_path("proj1", True)
        self.assertEqual(p_path, op.join(self.tempdir_path, "root/Projects/proj1"))
        self.assertTrue(op.exists(p_path))

        basket.resolve_project_path("proj1", False)  # not raise
        with self.assertRaises(dpError):
            basket.resolve_project_path("proj2", False)

    def test_resolve_project_path_path(self):
        true_path = op.join(self.tempdir_path, "proj1")
        p_path = basket.resolve_project_path(true_path, True)
        self.assertEqual(p_path, true_path)
        self.assertTrue(op.exists(p_path))

        basket.resolve_project_path(true_path, False)  # not raise
        with self.assertRaises(dpError):
            basket.resolve_project_path(op.join(self.tempdir_path, "proj2"), False)

    def test_resolve_project_path_dot(self):
        true_path = op.join(self.tempdir_path, "proj1")
        os.mkdir(true_path)
        with chdir(true_path):
            p_path = basket.resolve_project_path(".", True)
        self.assertEqual(p_path, true_path)

    def test_resolve_project_path_dots(self):
        true_path = op.join(self.tempdir_path, "proj1")
        work_dir = op.join(true_path, "work")
        os.makedirs(work_dir)
        with chdir(work_dir):
            p_path = basket.resolve_project_path("..", True)
        self.assertEqual(p_path, true_path)
