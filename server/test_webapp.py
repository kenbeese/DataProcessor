# coding: utf-8

import webapp
import sys
import os


sys.path = ([sys.path[0]]
            + [os.path.join(os.path.dirname(__file__), "../lib")]
            + sys.path[1:])
import dataprocessor as dp
sys.path = [sys.path[0]] + sys.path[2:]


class WebappTestCase(dp.tests.helper.TestEnvironment):

    def setUp(self):
        super(WebappTestCase, self).setUp()
        webapp.app.config["DATA_PATH"] = dp.rc.get_configure(
            dp.rc.rc_section, "json")
        self.app = webapp.app.test_client()

    def test_projectlistpage(self):
        rv = self.app.get('/')
        self.assertIn('<h2>Project List</h2>', rv.data)
        self.assertIn('<th>Name</th>', rv.data)
        self.assertIn('<th>Comment</th>', rv.data)
        self.assertIn('<th>Path</th>', rv.data)

    def test_ipynblistpage(self):
        rv = self.app.get('/ipynblist')
        self.assertIn('<h2>IPython Notebooks</h2>', rv.data)
        self.assertIn('<th>Name</th>', rv.data)
        self.assertIn('<th>Comment</th>', rv.data)
        self.assertIn('<th>Last modified</th>', rv.data)
        self.assertIn('<th>Tags</th>', rv.data)
        self.assertIn('<th>Path</th>', rv.data)

    def test_runpage(self):
        run_nodes = dp.filter.node_type(self.node_list, "run")
        for n in run_nodes:
            rv = self.app.get('/node/' + n['path'][1:])
            # For page header
            self.assertIn("<h2>{}</h2>".format(n['name']), rv.data)
            self.check_tag(n["parents"], rv.data)

    def test_projectpage(self):
        project_nodes = dp.filter.node_type(self.node_list, "project")
        for n in project_nodes:
            rv = self.app.get('/node/' + n['path'][1:])
            # For page header
            self.assertIn("<h2>{}</h2>".format(n['name']), rv.data)
            self.check_tag(n["parents"], rv.data)

    def check_tag(self, paths, data):
        for p in paths:
            n = dp.nodes.get(self.node_list, p)
            self.assertIn("{}</a>".format(n["name"]), data)
