#encoding:utf-8
import os.path as op


class InfoManager(object):
    """
    if specified optional, return elementTree object.

    Usage:
    >>> ### Add some data from path. ###
    >>> info = InfoManager()
    >>> diclist = [{"path":"/tmp/run01", "date":"1982/9/32",
    ...     "children": ["/tmp/hoge", "/tmp/hogehoge/"], "tags":["hoge", "hoges"]},
    ...     {"path":"/tmp/run02"}, {"path":"/tmp/run03"}]
    >>> node_list = info.metaPipe(diclist) # Add some data to list
    >>> node_list[0] == {'path': '/tmp/run01',
    ...     'name': 'run01', 'type': 'unknown',
    ...     'comment': '', 'date': '1982/9/32',
    ...     'tags': ['hoge', 'hoges'], 'parents': [], 'children': ["/tmp/hoge", "/tmp/hogehoge/"],
    ...     'evaluation': ''}
    True
    >>> node_list[1] == {'path': '/tmp/run02',
    ...     'name': 'run02', 'type': 'unknown',
    ...     'comment': '', 'date': '',
    ...     'tags': [], 'parents': [], 'children': [], 'evaluation': ''}
    True
    >>> node_list[2] == {'path': '/tmp/run03',
    ...     'name': 'run03', 'type': 'unknown',
    ...     'comment': '', 'date': '',
    ...     'tags': [], 'parents': [], 'children': [], 'evaluation': ''}
    True
    >>>
    >>> ### edit some elements and save. ###
    >>> node_list[1]["comment"] = "I am sleepy"
    >>> node_list[1] == {'path': '/tmp/run02',
    ...     'name': 'run02', 'type': 'unknown',
    ...     'comment': 'I am sleepy', 'date': '',
    ...     'tags': [], 'parents': [], 'children': [], 'evaluation': ''}
    True
    >>> info.dlist2xmlTree(node_list) # transform list to xmltree
    >>> info.saveInfo("/tmp/hoge.xml")
    >>>
    >>> ### scan metadata xml. ###
    >>> filestring = '''<?xml version="1.0" encoding="utf-8"?>
    ... <data>
    ...   <node path="/tmp/testrun/run01" name="run01" type="run">
    ...     <tags>
    ...       <tag>yes</tag>
    ...       <tag>ばか</tag>
    ...       <tag>ahohage</tag>
    ...     </tags>
    ...     <comment>hogecommet</comment>
    ...     <date>1987/05/12</date>
    ...     <evaluation/>
    ...     <parents>
    ...     </parents>
    ...     <children>
    ...     </children>
    ...   </node>
    ...
    ...   <node path="/tmp/testrun" name="hogeproject" type="project">
    ...     <tags>
    ...       <tag>yes</tag>
    ...       <tag>ahohage</tag>
    ...     </tags>
    ...     <comment>hogecommet</comment>
    ...     <date>1987/05/12</date>
    ...     <evaluation/>
    ...     <parents>
    ...        <link>/hogehoge/home/</link>
    ...     </parents>
    ...     <children>
    ...     </children>
    ...   </node>
    ...   <node path="/tmp/testrun2" name="hogehoge2" type="hyahha-">
    ...   <tags/><comment/> <date>1987/05/12</date><evaluation/><parents>
    ...     </parents>     <children>     </children> </node> </data>'''
    >>> f = open("/tmp/test.xml", "w")
    >>> f.write(filestring)
    >>> f.close()
    >>> info = InfoManager("/tmp/test.xml")
    >>> info.read()             # read xml
    >>> diclist = []
    >>> info.scanMeta(diclist) == [{'comment': 'hogecommet', 'evaluation': '', 'parents': [],
    ...     'name': 'run01', 'tags': ['yes', u'\u3070\u304b', 'ahohage'], 'date':
    ...     '1987/05/12', 'path': '/tmp/testrun/run01', 'type': 'run', 'children': []},
    ...     {'comment': 'hogecommet', 'evaluation': '', 'parents': ['/hogehoge/home/'],
    ...     'name': 'hogeproject', 'tags': ['yes', 'ahohage'], 'date': '1987/05/12',
    ...     'path': '/tmp/testrun', 'type': 'project', 'children': []},
    ...     {'comment': '', 'evaluation': '', 'parents': [], 'name': 'hogehoge2', 'tags': [],
    ...     'date': '1987/05/12', 'path': '/tmp/testrun2', 'type': 'hyahha-', 'children': []}]
    True
    >>> info.saveInfo()
    """

    def __init__(self, info_path="metainfo.xml", root_path="."):
        import xml.etree.ElementTree as ET
        self.tree = ET.ElementTree(ET.Element("data"))
        self.root_element = self.tree.find(root_path)
        self.info_path = op.abspath(info_path)
        self.node_nm = "node"
        self.path = "path"
        self.tags_nm = "tags"
        self.tag_nm = "tag"
        self.cmnt = "comment"
        self.parents = "parents"
        self.children = "children"
        self.name = "name"
        self.link = "link"
        self.evaluation = "evaluation"
        self.date = "date"
        self.node_type = "type"

    def read(self, info_path=None, root_path="."):
        import etreeio
        if info_path is not None:
            self.info_path = op.abspath(info_path)
        self.tree, self.root_element = etreeio.read(self.info_path, root_path)

    def __path2elem(self, path):
        for elem in list(self.root_element):
            if elem.get("path") == path:
                return elem
        self.addNode(path)
        return None

    def __elem2dict(self, elem):
        path = elem.get("path")
        name = elem.get("name")
        node_type = elem.get("type")
        tags = [self.normalizeWhiteSpace(tag.text)
                for tag in elem.find(self.tags_nm).findall(self.tag_nm)]
        comment = self.normalizeWhiteSpace(elem.findtext(self.cmnt))
        date = self.normalizeWhiteSpace(elem.findtext(self.date))
        parents = [parent.text for parent in elem.find(self.parents).findall(self.link)]
        children = [child.text for child in elem.find(self.children).findall(self.link)]
        evaluation = self.normalizeWhiteSpace(elem.findtext(self.evaluation))
        # print path, name, node_type, tags, comment, date, parents, children, evaluation
        return {self.path: path, self.name: name,
                self.node_type: node_type, self.tags_nm: tags,
                self.evaluation: evaluation,
                self.cmnt: comment, self.date: date,
                self.parents: parents, self.children: children}

    def normalizeWhiteSpace(self, string):
        import re
        reg = re.compile("\s+")
        try:
            return reg.sub(" ", string).strip()
        except TypeError:
            return None

    def scanMeta(self, node_list):
        node_list = []
        for node in list(self.root_element):
            piped = self.__elem2dict(node)
            node_list.append(piped)
        return node_list

    def dlist2xmlTree(self, dlist):
        import xml.etree.ElementTree as ET
        self.tree = ET.ElementTree(ET.Element("data"))
        self.root_element = self.tree.getroot()
        for dic in dlist:
            self.addNode(**dic)

    def metaPipe(self, node_list):
        self.dlist2xmlTree(node_list)
        return self.scanMeta(node_list)

    def saveInfo(self, out_path=None):
        """
        if info_path is not specified, meta data is written in read file.
        """
        import etreeio
        if out_path is None:
            out_path = self.info_path
        else:
            out_path = op.abspath(out_path)
        etreeio.write(self.tree, out_path)
        return

    def addNode(self, path, name=None, type="unknown", comment="", tags=[],
                date="", parents=[], children=[], evaluation=""):
        import xml.etree.ElementTree as ET
        import os.path
        for node in list(self.root_element):
            if node.get("path") == path:
                raise Warning("%s exists already." % path)
        if name is None:
            name = os.path.basename(path)
        node = ET.SubElement(self.root_element, self.node_nm, {"path": path,
                                                               "name": name,
                                                       "type": type})
        ET.SubElement(node, self.cmnt).text = comment
        ET.SubElement(node, self.date).text = date
        ET.SubElement(node, self.evaluation).text = evaluation

        tags_ele = ET.SubElement(node, self.tags_nm)
        for tag in tags:
            ET.SubElement(tags_ele, self.tag_nm).text = tag

        parents_ele = ET.SubElement(node, self.parents)
        for parent in parents:
            ET.SubElement(parents_ele, self.link).text = parent

        children_ele = ET.SubElement(node, self.children)
        for child in children:
            ET.SubElement(children_ele, self.link).text = child


def addRunsMeta(run_list):
    info = InfoManager()
    run_list = info.metaPipe(run_list)
    return run_list


def scanMeta(run_list, info_path):
    info = InfoManager(info_path)
    info.read()
    run_list = info.scanPipe(run_list)
    return run_list


def register(pipes_dics):
    pipes_dics["add_meta"] = {
        "func": addRunsMeta,
        "args": [],
        "desc": "add run meta-data"}
    pipes_dics["scan_meta"] = {
        "func": scanMeta,
        "args": ["info_path"],
        "desc": "scan meta-data"}


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
