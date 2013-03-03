class InfoManager(object):
    """
    if specified optional, return elementTree object.

    Usage:


    >>> filestring = '''<?xml version="1.0" encoding="utf-8"?>
    ... <data>
    ...
    ...   <run name="run01">
    ...     <tags>
    ...       <tag>yes</tag>
    ...       <tag>no</tag>
    ...       <tag>ahohage</tag>
    ...     </tags>
    ...     <comment>hogecommet</comment>
    ...     <date>1987/05/12</date>
    ...     <optional></optional>
    ...   </run>
    ...
    ...   <run name="run02">
    ...     <tags>
    ...       <tag>tag1</tag>
    ...       <tag>tag3 </tag>
    ...     </tags>
    ...     <comment>come</comment>
    ...     <date>1989/03/12</date>
    ...   </run>
    ...   <run name="run03"><tags>  <tag> tag321   hoge</tag>   <tag>tag5</tag>  </tags> <comment>hagehagehage</comment>
    ... <date>1988/02/03 </date></run></data>
    ... '''
    >>> f = open("/tmp/test.xml", "w")
    >>> f.write(filestring)
    >>> f.close()
    >>> import os.path as op
    >>> info = InfoManager("/tmp/test.xml")
    >>> info.humanReadable("/tmp/human.xml")
    >>> diclist = [{"path":"/tmp/run01"}, {"path":"/tmp/run02"}, {"path":"/tmp/run03"}]
    >>> info.metaPipe(diclist)[1] == {'path': '/tmp/run02',
    ...     'meta': {'comment': 'come', 'date': '1989/03/12',
    ...         'optional': None,
    ...         'tags': ['tag1', 'tag3']}}
    True
    >>> info.metaPipe(diclist)[2] == {'path': '/tmp/run03',
    ...     'meta': {'comment': 'hagehagehage', 'date': '1988/02/03',
    ...         'optional': None,
    ...         'tags': ['tag321 hoge', 'tag5']}}
    True
    >>> info.taglist()
    [' tag321   hoge', 'ahohage', 'no', 'tag1', 'tag3 ', 'tag5', 'yes']
    >>> info.runnamelist()
    ['run01', 'run02', 'run03']
    >>> info.runInfo('run03') == {'comment': 'hagehagehage', 'date': '1988/02/03',
    ...     'optional': None,
    ...     'tags': ['tag321 hoge', 'tag5']}
    True
    >>> info.setComment('run03', "test")
    >>> info.runInfo('run03')["comment"]
    'test'
    >>> info.setTag('run03', "newtag")
    >>> info.runInfo('run03')["tags"]
    ['tag321 hoge', 'tag5', 'newtag']
    >>> info.rmTag('run03', "newtag")
    >>> info.runInfo('run03')["tags"]
    ['tag321 hoge', 'tag5']
    >>> info.rmTag('run03', "tag5")
    >>> info.setComment('run03', "testdayo~")
    >>> info.setTag('run02', "testdayo~")
    >>> info.saveInfo('/tmp/hoge')
    >>> info.addRun('run10')
    >>> info.setTag('run10', "test2dayo")
    >>> info.saveInfo()
    >>> import os
    >>> os.remove("/tmp/hoge")
    """


    def __init__(self, info_path, root_path="."):
        import xml.etree.ElementTree as ET
        import os.path as op
        self.info_path = op.abspath(info_path)
        self.tree = ET.parse(self.info_path)
        root = self.tree.getroot()
        self.root = root.find(root_path)
        self.run_nm = "run"
        self.tags_nm = "tags"
        self.tag_nm = "tag"
        self.cmnt = "comment"
        self.opt = "optional"
        self.date = "date"
        self.metakey = "meta"



    def __path2elem(self, path):
        import os.path as op
        path_key = op.relpath(path, op.dirname(self.info_path))
        for elem in list(self.root):
            if elem.get("name") == path_key:
                return elem
        return None


    def __elem2dict(self, elem):
        tags = [self.normWhiteSpace(tag.text)
                for tag in elem.find(self.tags_nm).findall(self.tag_nm)]
        comment = self.normWhiteSpace(elem.findtext(self.cmnt))
        date = self.normWhiteSpace(elem.findtext(self.date))
        opt = elem.find(self.opt)

        return {self.tags_nm: tags, self.cmnt:comment, self.date: date, self.opt: opt}


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
        return run name list written in info_path.
        """
        l = [run.get("name") for run in list(self.root)
             for tag in run.find(self.tags_nm).findall(self.tag_nm)
             if self.normWhiteSpace(tag.text) == self.normWhiteSpace(tagbody)]
        return l


    def runnamelist(self):
        """
        return run name list written in info_path.
        """
        l = [run.get("name") for run in list(self.root)]
        return l


    def runInfo(self, runname):
        """
        return run infomation, for example, comment, tag, date, etc.
        """
        for elem in list(self.root):
            if elem.get("name") == runname:
                return self.__elem2dict(elem)


    def setComment(self, runname, comment):
        for elem in list(self.root):
            if elem.get("name") == runname:
                com = elem.find(self.cmnt)
                com.text = comment


    def setTag(self, runname, tagbody):
        import xml.etree.ElementTree as ET
        for elem in list(self.root):
            if elem.get("name") == runname:
                tags = elem.find(self.tags_nm)
                for tag in tags.findall(self.tag_nm):
                    if tag.text == self.normWhiteSpace(tagbody):
                        raise Warning("%s was already defined." & tagbody)
                newtag = ET.SubElement(tags, self.tag_nm)
                newtag.text = self.normWhiteSpace(tagbody)


    def rmTag(self, runname, tagbody):
        for elem in list(self.root):
            if elem.get("name") == runname:
                tags = elem.find(self.tags_nm)
                for tag in tags.findall(self.tag_nm):
                    if tag.text == self.normWhiteSpace(tagbody):
                        tags.remove(tag)
                        return
                raise Warning("%s was not defined." % tagbody)


    def metaPipe(self, run_list):
        pipedList = []
        for dic in run_list:
            elem = self.__path2elem(dic["path"])
            if elem != None:
                piped = {self.metakey:self.__elem2dict(elem)}
                piped.update(dic)
                pipedList.append(piped)
            else:
                print("Warning: meta data for directory %s is not defined." % dic["path"])
        return pipedList


    def saveInfo(self, info_path = None):
        """
        if info_path is not specified, meta data is written in read file.
        """
        import os.path
        if info_path == None:
            info_path = self.info_path
        else:
            info_path = os.path.abspath(info_path)
        self.tree.write(info_path)
        return




    def humanReadable(self, out_path = None):
        import os.path

        if out_path == None:
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

    def addRun(self, runname):
        import xml.etree.ElementTree as ET

        for run in list(self.root):
            if run.get("name") == runname:
                raise Warning("%s exists already." % runname)
        run = ET.SubElement(self.root, self.run_nm, {"name":runname})
        ET.SubElement(run, self.cmnt)
        ET.SubElement(run, self.tags_nm)
        ET.SubElement(run, self.opt)
        ET.SubElement(run, self.date)





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
    if reg1.search(string) == None:
        return string
    else:
        string = reg1.sub(r"<\1>\n<\2>", string, 1)
        return _splitTag(string)

def _addNewline(string):
    import re
    reg1 = re.compile(r"(</run>[ \t\b]*[\n\r])(\S+)")
    if reg1.search(string) == None:
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


def addRunsMeta(run_list, info_path):
    info = InfoManager(info_path)
    run_list = info.metaPipe(run_list)
    return run_list


def register(pipes_dics):
    pipes_dics["run_meta"] = {
        "func" : addRunsMeta,
        "args" : ["info_path"],
        "desc" : "add run meta-data",
        }


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
