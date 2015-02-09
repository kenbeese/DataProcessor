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
        for node in self.node_list:
            if node["type"] in _TAG_EDITABLE_NODETYPE:
                for tag_path in node["parents"]:
                    rv = self.untag(node["path"], tag_path)
                    # tag 以外のにも引っかかるのを何とかする
                    self.assertNotIn(tag_path, rv.data)

    def add_tag(self, path, tagname):
        return self.app.post('/add_tag' + path,
                             data=dict(tagname=tagname),
                             follow_redirects=True)

    def untag(self, path, tag_path):
        return self.app.get('/untag' + path + '?tag_path=' + tag_path)

    def check_name_and_link(self, paths, data):
        for p in paths:
            n = dp.nodes.get(self.node_list, p)
            self.assertIn(
                "<a href='{}'>{}</a>".format(n["path"], n["name"]), data)
