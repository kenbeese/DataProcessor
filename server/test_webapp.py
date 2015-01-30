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

    def test_projectpage(self):
        rv = self.app.get('/')
        self.assertIn(
            '<a class="navbar-brand" href="/">DataProcessor</a>', rv.data)
        self.assertIn('<a class="dp-nav" href="/">Project List</a>', rv.data)
        self.assertIn(
            '<a class="dp-nav" href="/ipynblist">IPython Notebooks</a>', rv.data)
        self.assertIn('<th>Name</th>', rv.data)
        self.assertIn('<th>Comment</th>', rv.data)
        self.assertIn('<th>Path</th>', rv.data)
