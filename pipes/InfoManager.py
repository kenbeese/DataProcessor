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
    ...       <tag>tag3</tag>
    ...     </tags>
    ...     <comment>come</comment>
    ...     <date>1989/03/12</date>
    ...   </run>
    ...
    ...   <run name="run03">
    ...     <tags>
    ...       <tag>tag321</tag>
    ...       <tag>tag5</tag>
    ...     </tags>
    ...     <comment>hagehagehage</comment>
    ...     <date>1988/02/03</date>
    ...   </run>
    ...
    ... </data>
    ... '''
    >>> f = open("/tmp/test.xml", "w")
    >>> f.write(filestring)
    >>> f.close()
    >>> import os.path as op
    >>> info = InfoManager("/tmp/test.xml")
    >>> diclist = [{"path":"/tmp/run01"}, {"path":"/tmp/run02"}]
    >>> info.metaPipe(diclist)[1] == {'path': '/tmp/run02',
    ...     'meta': {'comment': 'come', 'date': '1989/03/12',
    ...         'optional': None,
    ...         'tags': ['tag1', 'tag3']}}
    True
    >>> import os
    >>> os.remove("/tmp/test.xml")
    """

    def __init__(self, info_path):
        import xml.etree.ElementTree as ET
        import os.path as op
        self.info_path = op.abspath(info_path)
        tree = ET.parse(self.info_path)
        self.root = tree.getroot()
        self.tags_nm = "tags"
        self.tag_nm = "tag"
        self.cmnt = "comment"
        self.opt = "optional"
        self.date = "date"
        self.metakey = "meta"

    def __path2elem(self, path):
        import os.path as op
        path_key = op.relpath(path, op.dirname(self.info_path))
        for elem in self.root.iter():
            if elem.get("name") == path_key:
                return elem
        return None

    def __elem2dict(self, elem):
        tags = [tag.text for tag in elem.find(self.tags_nm).findall(self.tag_nm)]
        comment = elem.findtext(self.cmnt)
        date = elem.findtext(self.date)
        opt = elem.find(self.opt)

        return {self.tags_nm: tags, self.cmnt:comment, self.date: date, self.opt: opt}


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



def addRunsMeta(run_list, info_path):
    info = InfoManager(info_path)
    run_list = info.metaPipe(run_list)
    return run_list


def register(pipes_dics):
    pipes_dics["run_meta"] = {
        "func" : addRunsMeta,
        "args" : ["info_path"],
        "desc" : "add run meta-data"
        }


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
