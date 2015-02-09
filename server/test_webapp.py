# coding: utf-8

import webapp
import sys
import os
from pyquery import PyQuery as PQ

sys.path = ([sys.path[0]]
            + [os.path.join(os.path.dirname(__file__), "../lib")]
            + sys.path[1:])
import dataprocessor as dp
sys.path = [sys.path[0]] + sys.path[2:]


_TAG_EDITABLE_NODETYPE = ["run", "project"]


class WebappTestCase(dp.tests.helper.TestEnvironment):

    def setUp(self):
        super(WebappTestCase, self).setUp()
        webapp.app.config["DATA_PATH"] = dp.rc.get_configure(
            dp.rc.rc_section, "json")
        webapp.app.config["SECRET_KEY"] = "development key"
        self.app = webapp.app.test_client()

    def test_projectlistpage(self):
        rv = self.app.get('/')
        query = PQ(rv.data)
        # check page name
        self.assertEqual('Project List', query("h2").text())
        # check number of project
        self.assertEqual(len(dp.filter.node_type(self.node_list, "project")),
                         len(query("table > tbody > tr")))

    def test_ipynblistpage(self):
        rv = self.app.get('/ipynblist')
        query = PQ(rv.data)
        # check page name
        self.assertEqual('IPython Notebooks', query("h2").text())
        # check number of ipython notebook
        self.assertEqual(len(dp.filter.node_type(self.node_list, "ipynb")),
                         len(query("table>tbody>tr")))

    def test_nodepage(self):
        nodes = dp.filter.node_type(self.node_list, "run")
        for n in nodes:
            rv = self.app.get('/node' + n['path'])
            query = PQ(rv.data)
            # check page name
            self.assertEqual(n["name"], query("h2").text())

    def test_add_tag(self):
        for node in self.node_list:
            if node["type"] in _TAG_EDITABLE_NODETYPE:
                rv = self.add_tag(node["path"], "new added tag")
                query = PQ(rv.data)
                self.assertEqual("Added tag 'new added tag'",
                                 query("nav.navbar p.navbar-text").text())

    def test_untag(self):
        for node in [n for n in self.node_list]:
            if node["type"] in _TAG_EDITABLE_NODETYPE:

                self.add_tag(node["path"], "test_tag")
                tag_path = dp.rc.resolve_project_path("test_tag", False)

                rv = self.untag(node["path"], tag_path)
                query = PQ(rv.data)

                self.assertEqual("Removed tag 'test_tag'",
                                 query("nav.navbar p.navbar-text").text())

                # get tags
                tags = query("dt + dd>p>span.label>a:eq(0)")
                if tags:
                    self.assertNotIn(tag_path, tags.attr("href"))

    def add_tag(self, path, tagname):
        return self.app.post('/add_tag' + path,
                             data=dict(tagname=tagname),
                             follow_redirects=True)

    def untag(self, path, tag_path):
        path = "/untag" + path + "?tag_path=" + tag_path
        return self.app.get(path, follow_redirects=True)
