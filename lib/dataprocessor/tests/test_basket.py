# coding: utf-8

from . import helper
from .. import basket
from ..utility import chdir

import os
import os.path as op


class TestBasket(helper.TestEnvironment):

    def test_resolve_project_path_name(self):
        p_path = basket.resolve_project_path("proj1")
        self.assertEqual(p_path, op.join(self.tempdir_path, "root/Projects/proj1"))

    def test_resolve_project_path_path(self):
        true_path = op.join(self.tempdir_path, "proj1")
        p_path = basket.resolve_project_path(true_path)
        self.assertEqual(p_path, true_path)

    def test_resolve_project_path_dot(self):
        true_path = op.join(self.tempdir_path, "proj1")
        os.mkdir(true_path)
        with chdir(true_path):
            p_path = basket.resolve_project_path(".")
        self.assertEqual(p_path, true_path)

    def test_resolve_project_path_dots(self):
        true_path = op.join(self.tempdir_path, "proj1")
        work_dir = op.join(true_path, "work")
        os.makedirs(work_dir)
        with chdir(work_dir):
            p_path = basket.resolve_project_path("..")
        self.assertEqual(p_path, true_path)
