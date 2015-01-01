# coding=utf-8
"""Utility of test."""

import unittest
import tempfile
import os
import os.path as op
import shutil
from jinja2 import Template

from .. import nodes


yaml_template = Template("""
{{section_name}}:
{% for key, val in setting %}
    {{key}}: {{val}}
{% endfor %}
""")

ini_template = Template("""
[((section_name))]
{% for key, val in setting %}
{{key}}={{val}}
{% endfor %}
""")

nosection_template = Template("""
{% for key, val in setting %}
{{key}}={{val}}
{% endfor %}
""")


class TestNodeListAndDir(unittest.TestCase):

    """Unittest for using node_list and directory.

    create node_list including following nodes.


    ===============   =========  ======== =========
    path              node_type  name     conf_file
    ===============   =========  ======== =========
    tmpdir/p1         project    p1       None
    tmpdir/p1/run00   run        run00    parameters.yml
    tmpdir/p1/run01   run        run01    parameters.ini
    tmpdir/p1/run02   run        run02    parameters.yaml
    tmpdir/p2         project    p2       None
    tmpdir/p2/run00   run        run00    param.conf (INI)
    tmpdir/p2/run01   run        run01    run.cfg (no section)
    ===============   =========  ======== ==========

    Attributes
    ----------
    tempdir_path : str
        temporally directory path
    project_paths : list
        list of project path
    node_list : list

    """

    def setUp(self):
        self.tempdir_path = tempfile.mkdtemp()
        self.project_paths = []
        self.node_list = []
        self._create_project_and_run("p1", rundir_num=3)
        self._create_project_and_run("p2", rundir_num=2)

    def tearDown(self):
        shutil.rmtree(self.tempdir_path)

    def _create_project_and_run(self, project_name, rundir_num=2):
        p_path = os.path.join(self.tempdir_path, project_name)
        self._create_project_or_run(p_path)

        for i in range(rundir_num):
            path = os.path.join(p_path, "run%02d" % i)
            self._create_project_or_run(path, type="run", parents=[p_path])

    def _create_project_or_run(self, path, type="project", parents=[],
                               children=[]):
        os.mkdir(path)
        if type == "project":
            self.project_paths.append(path)

        node = {"path": path,
                "type": type,
                "name": os.path.basename(path),
                "children": children,
                "parents": parents}
        nodes.add(self.node_list, node)

    def _place_conf_files(self):
        def _create_conf_file(tmpl, fn, name, cfg):
            with open(op.join(path, fn)) as f:
                f.write(tmpl.render(section_name=name, setting=cfg))

        for node in self.node_list:
            path = node["path"]
            if path.endswith("p1/run00"):
                _create_conf_file(yaml_template, "parameters.yml",
                                  "parameters", {"A": 1.0, "N": 100})
                continue
            if path.endswith("p1/run01"):
                _create_conf_file(ini_template, "parameters.ini",
                                  "parameters", {"A": 1.0, "N": 100})
                continue
            if path.endswith("p1/run02"):
                _create_conf_file(yaml_template, "parameters.yaml",
                                  "parameters", {"A": 1.0, "N": 100})
                continue
            if path.endswith("p2/run00"):
                _create_conf_file(ini_template, "param.conf",
                                  "param", {"A": 1.0, "N": 100})
                continue
            if path.endswith("p2/run01"):
                _create_conf_file(nosection_template, "run.cfg",
                                  "", {"A": 1.0, "N": 100})
                continue
