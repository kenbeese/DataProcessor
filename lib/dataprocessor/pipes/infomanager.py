#encoding:utf-8
import os.path
import xml.etree.ElementTree as ET


class InfoManager(object):
    """
    if specified optional, return elementTree object.

    Usage:
    >>> ### fill incomplete node_list. ###
    >>> info = InfoManager()
    >>> diclist = [{"path":"/tmp/run01", "date":"1982/9/32",
    ...     "children": ["/tmp/hoge", "/tmp/hogehoge/"],
    ...     "tags":["hoge", "hoges"]},
    ...     {"path":"/tmp/run02"}, {"path":"/tmp/run03"}]
    >>> info.node_list2etree(diclist) # incomplete node_list -> complete etree
    >>> node_list = info.etree2node_list()
    >>> node_list[0] == {'path': '/tmp/run01',
    ...     'name': 'run01', 'type': 'unknown',
    ...     'comment': '', 'date': '1982/9/32',
    ...     'tags': ['hoge', 'hoges'], 'parents': [],
    ...     'children': ["/tmp/hoge", "/tmp/hogehoge/"],
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
    >>>
    >>> ### edit some elements and save. ###
    >>> node_list[1]["comment"] = "I am sleepy"
    >>> node_list[1] == {'path': '/tmp/run02',
    ...     'name': 'run02', 'type': 'unknown',
    ...     'comment': 'I am sleepy', 'date': '',
    ...     'tags': [], 'parents': [], 'children': [], 'evaluation': ''}
    True
    >>> info.node_list2etree(node_list) # transform node list to etree
    >>> info.save("/tmp/hoge.xml")
    >>>
    >>>
    >>> ### scan metadata xml. ###
    >>> info = InfoManager()
    >>> info.read("/tmp/hoge.xml")             # read xml
    >>> node_list = info.etree2node_list()     # output node_list format
    >>> node_list[1] == {'path': '/tmp/run02',
    ...     'name': 'run02', 'type': 'unknown',
    ...     'comment': 'I am sleepy', 'date': '',
    ...     'tags': [], 'parents': [], 'children': [], 'evaluation': ''}
    True
    >>> info.node_list2etree(node_list)
    >>> node_list = info.etree2node_list()
    >>> info.save("/tmp/test.xml")
    """

    def __init__(self, root_path="."):
        self.tree = ET.ElementTree(ET.Element("data"))
        self.root_element = self.tree.find(root_path)
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

    def read(self, read_path, root_path="."):
        import etreeio
        fpath = os.path.abspath(read_path)
        self.tree, self.root_element = etreeio.read(fpath, root_path)

    def __element2node(self, elem):
        path = elem.get(self.path)
        name = elem.get(self.name)
        node_type = elem.get(self.node_type)
        tags = [self.normalize_white_space(tag.text)
                for tag in elem.find(self.tags_nm).findall(self.tag_nm)]
        comment = self.normalize_white_space(elem.findtext(self.cmnt))
        date = self.normalize_white_space(elem.findtext(self.date))
        parents = [parent.text for parent
                   in elem.find(self.parents).findall(self.link)]
        children = [child.text for child
                    in elem.find(self.children).findall(self.link)]
        evaluation = self.normalize_white_space(elem.findtext(self.evaluation))
        return {self.path: path, self.name: name,
                self.node_type: node_type, self.tags_nm: tags,
                self.evaluation: evaluation,
                self.cmnt: comment, self.date: date,
                self.parents: parents, self.children: children}

    def normalize_white_space(self, string):
        import re
        reg = re.compile("\s+")
        try:
            return reg.sub(" ", string).strip()
        except TypeError:
            return None

    def etree2node_list(self):
        node_list = []
        for node_element in list(self.root_element):
            node = self.__element2node(node_element)
            node_list.append(node)
        return node_list

    def node_list2etree(self, node_list):
        import xml.etree.ElementTree as ET
        self.tree = ET.ElementTree(ET.Element("data"))
        self.root_element = self.tree.getroot()
        for node in node_list:
            self.add_node2etree(**node)

    def save(self, out_path):
        import etreeio
        etreeio.write(self.tree, out_path)
        return

    def add_node2etree(self, path, name=None, type="unknown", comment="",
                       tags=[], date="", parents=[], children=[],
                       evaluation=""):
        for node in list(self.root_element):
            if node.get("path") == path:
                raise Warning("%s exists already." % path)
        if name is None:
            name = os.path.basename(path)
        node = ET.SubElement(self.root_element, self.node_nm, {self.path: path,
                                                               self.name: name,
                                                               self.node_type: type})
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


def fill_node_list(node_list):
    info = InfoManager()
    info.node_list2etree(node_list)
    return info.etree2node_list()


def scan_meta(node_list, info_path):
    info = InfoManager()
    info.read(info_path)
    node_list = node_list.append(info.etree2node_list())
    return node_list


def save_node_list(node_list, out_file):
    info = InfoManager()
    info.node_list2etree(node_list)
    info.save(out_file)


def register(pipes_dics):
    pipes_dics["fill_meta"] = {
        "func": fill_node_list,
        "args": [],
        "desc": "add run meta-data"}
    pipes_dics["scan_meta"] = {
        "func": scan_meta,
        "args": ["info_path"],
        "desc": "scan meta-data"}
    pipes_dics["save_meta"] = {
        "func": save_node_list,
        "args": ["out_path"],
        "desc": "save meta-data"}


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
