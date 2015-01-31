# coding: utf-8

import webapp
import sys
import os


sys.path = ([sys.path[0]]
            + [os.path.join(os.path.dirname(__file__), "../lib")]
            + sys.path[1:])
import dataprocessor as dp
sys.path = [sys.path[0]] + sys.path[2:]


tag_edit_nodetypes = ["run", "project"]


class WebappTestCase(dp.tests.helper.TestEnvironment):

    def setUp(self):
        super(WebappTestCase, self).setUp()
        webapp.app.config["DATA_PATH"] = dp.rc.get_configure(
            dp.rc.rc_section, "json")
        webapp.app.config["SECRET_KEY"] = "development key"
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

    def test_nodepage(self):
        nodes = dp.filter.node_type(self.node_list, "run")
        for n in nodes:
            rv = self.app.get('/node' + n['path'])
            self.assertIn("<h2>{}</h2>".format(n['name']), rv.data)

    def test_add_tag(self):
        for node in self.node_list:
            if node["type"] in tag_edit_nodetypes:
                rv = self.add_tag(node["path"], "new added tag")
                # tag 以外のにも引っかかるのを何とかする
                self.assertIn("new added tag", rv.data)

    def test_untag(self):
        for node in self.node_list:
            if node["type"] in tag_edit_nodetypes:
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
