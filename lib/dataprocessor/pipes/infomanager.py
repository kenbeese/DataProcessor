#encoding:utf-8


class InfoManager(object):
    """
    if specified optional, return elementTree object.

    Usage:
    >>> info = InfoManager()
    >>> diclist = [{"path":"/tmp/run01", "date":"1982/9/32",
    ...     "children": ["/tmp/hoge", "/tmp/hogehoge/"], "tags":["hoge", "hoges"]},
    ...     {"path":"/tmp/run02"}, {"path":"/tmp/run03"}]
    >>> node_list = info.metaPipe(diclist)
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
    >>> node_list[1]["comment"] = "I am sleepy"
    >>> node_list[1] == {'path': '/tmp/run02',
    ...     'name': 'run02', 'type': 'unknown',
    ...     'comment': 'I am sleepy', 'date': '',
    ...     'tags': [], 'parents': [], 'children': [], 'evaluation': ''}
    True
    >>> info.dlist2xmlTree(node_list)
    >>> info.saveInfo("/tmp/hoge.xml")
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
    >>> info.read()
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
        import os.path as op
        self.tree = ET.ElementTree(ET.Element("data"))
        root = self.tree
        self.root = root.find(root_path)
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
        import xml.etree.ElementTree as ET
        import os.path as op
        if info_path is not None:
            self.info_path = op.abspath(info_path)
        self.tree = ET.parse(self.info_path)
        root = self.tree.getroot()
        self.root = root.find(root_path)

    def __path2elem(self, path):
        for elem in list(self.root):
            if elem.get("path") == path:
                return elem
        self.addNode(path)
        return None

    def __elem2dict(self, elem):
        path = elem.get("path")
        name = elem.get("name")
        node_type = elem.get("type")
        tags = [self.normWhiteSpace(tag.text)
                for tag in elem.find(self.tags_nm).findall(self.tag_nm)]
        comment = self.normWhiteSpace(elem.findtext(self.cmnt))
        date = self.normWhiteSpace(elem.findtext(self.date))
        parents = [parent.text for parent in elem.find(self.parents).findall(self.link)]
        children = [child.text for child in elem.find(self.children).findall(self.link)]
        evaluation = self.normWhiteSpace(elem.findtext(self.evaluation))
        # print path, name, node_type, tags, comment, date, parents, children, evaluation
        return {self.path: path, self.name: name,
                self.node_type: node_type, self.tags_nm: tags,
                self.evaluation: evaluation,
                self.cmnt: comment, self.date: date,
                self.parents: parents, self.children: children}

    def normWhiteSpace(self, string):
        import re
        reg = re.compile("\s+")
        try:
            return reg.sub(" ", string).strip()
        except TypeError:
            return None

    def taglist(self):
        tag_list = [tag.text for tag in self.root.iter(self.tag_nm)]
        tag_list = list(set(tag_list))
        tag_list.sort()
        return tag_list

    def taggedlist(self, tagbody):
        """
        return path list written in info_path.
        """
        l = [node.get("path") for node in list(self.root)
             for tag in node.find(self.tags_nm).findall(self.tag_nm)
             if self.normWhiteSpace(tag.text) == self.normWhiteSpace(tagbody)]
        return l

    def nodelist(self):
        """
        return node path list written in info_path.
        """
        l = [node.get("path") for node in list(self.root)]
        return l

    def nodeInfo(self, path):
        """
        return node infomation, for example, comment, tag, date, etc.
        """
        for elem in list(self.root):
            if elem.get("path") == path:
                return self.__elem2dict(elem)

    def scanMeta(self, node_list):
        node_list = []
        for node in list(self.root):
            piped = self.__elem2dict(node)
            node_list.append(piped)
        return node_list

    def dlist2xmlTree(self, dlist):
        import xml.etree.ElementTree as ET
        self.tree = ET.ElementTree(ET.Element("data"))
        self.root = self.tree.getroot()
        for dic in dlist:
            self.addNode(**dic)

    def metaPipe(self, node_list):
        self.dlist2xmlTree(node_list)
        return self.scanMeta(node_list)

    def saveInfo(self, info_path=None):
        """
        if info_path is not specified, meta data is written in read file.
        """
        import os.path
        if info_path is None:
            info_path = self.info_path
        else:
            info_path = os.path.abspath(info_path)
            self.info_path = info_path
        self.tree.write(info_path, encoding="UTF-8")
        self.humanReadable(info_path)
        return

    def humanReadable(self, out_path=None):
        import os.path
        if out_path is None:
            out_path = self.info_path
        else:
            out_path = os.path.abspath(out_path)
        f = open(self.info_path)
        string = f.read()
        f.close()

        string = _rmindent(string)
        string = _splitTag(string)
        string = _addNewline(string)
        string = _indent(string)
        f = open(out_path, "w")
        f.write(string)
        f.close
        return

    def addNode(self, path, name=None, type="unknown", comment="", tags=[],
                date="", parents=[], children=[], evaluation=""):
        import xml.etree.ElementTree as ET
        import os.path
        for node in list(self.root):
            if node.get("path") == path:
                raise Warning("%s exists already." % path)
        if name is None:
            name = os.path.basename(path)
        node = ET.SubElement(self.root, self.node_nm, {"path": path,
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


def _rmindent(string):
    import re
    sp = re.compile("[\n\r]")
    lines = sp.split(string)
    string = ""
    for line in lines:
        if line != "":
            string = string + line.strip() + "\n"
    return string


def _splitTag(string):
    import re
    reg1 = re.compile(r"<(.*?)>[ \t\b]*<(.*?)>")
    if reg1.search(string) is None:
        return string
    else:
        string = reg1.sub(r"<\1>\n<\2>", string, 1)
        return _splitTag(string)


def _addNewline(string):
    import re
    reg1 = re.compile(r"(</run>[ \t\b]*[\n\r])(\S+)")
    if reg1.search(string) is None:
        return string
    else:
        string = reg1.sub(r"\1\n\2", string, 1)
        return _addNewline(string)


def _checkTag(line):
    import re
    startend = re.compile("<.+?>.*?</.+?>")
    end = re.compile("</.+?>")
    onetag = re.compile("<.+?/>")
    start = re.compile("<.+?>")
    if startend.search(line):
        return "startend"
    elif onetag.search(line):
        return "oneline"
    elif end.search(line):
        return "end"
    elif start.search(line):
        return "start"
    else:
        return "none"


def _indent(string):
    import re
    sp = re.compile("[\n\r]")
    lines = sp.split(string)
    string = ""
    depth = 0
    for line in lines:
        if line == "":
            string = string + "\n"
        else:
            if _checkTag(line) == "start":
                string = string + "  " * (depth) + line + "\n"
                depth = depth + 1
            elif _checkTag(line) == "end":
                depth = depth - 1
                string = string + "  " * (depth) + line + "\n"
            else:
                string = string + "  " * (depth) + line + "\n"
    return string


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
