# coding: utf-8

from . import helper
from ..pipes.add_tag import add_tag
from ..exception import DataProcessorError as dpError
from .. import filter as dpfilter


class TestAddTag(helper.TestEnvironment):

    def test_add_tag(self):
        runs = dpfilter.node_type(self.node_list, "run")
        projects = dpfilter.node_type(self.node_list, "project")
        for run in runs:
            path = run["path"]
            for project in projects:
                project_path = project["path"]
                if project_path not in run["parents"]:
                    # add new project
                    add_tag(self.node_list, path, project_path)
                    self.assertTrue(project_path in run["parents"])
                else:
                    # add exsiting project
                    add_tag(self.node_list, path, project_path)  # not raise

    def test_add_tag_new(self):
        runs = dpfilter.node_type(self.node_list, "run")
        new_tag = "_homhom_"
        for run in runs:
            path = run["path"]
            add_tag(self.node_list, path, new_tag)
        tagged_nodes = dpfilter.project(self.node_list, new_tag)
        self.assertItemsEqual(runs, tagged_nodes)

    def test_add_tag_itself(self):
        runs = dpfilter.node_type(self.node_list, "run")
        for run in runs:
            path = run["path"]
            with self.assertRaisesRegexp(dpError, "Cannot tag itself"):
                add_tag(self.node_list, path, path)

    def test_add_tag_nopath(self):
        projects = dpfilter.node_type(self.node_list, "project")
        with self.assertRaises(dpError):
            add_tag(self.node_list, "/nopath", projects[0])
        with self.assertRaises(dpError):
            add_tag(self.node_list, "/nopath", "/noproject")
