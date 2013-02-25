def main():
    import os.path as op
    info = InfoManager("test.xml")
    diclist = [{"path":op.abspath("run01")}]
    print info.metaPipe(diclist)


class InfoManager(object):
    """
    """

    def __init__(self, info_path):
        import xml.etree.ElementTree as ET
        import os.path as op
        tree = ET.parse(info_path)
        self.root = tree.getroot()
        self.info_path = op.abspath(info_path)
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


    def metaPipe(self, diclist):
        pipedList = []
        for dic in diclist:
            piped = {self.metakey:self.__elem2dict(self.__path2elem(dic["path"]))}
            piped.update(dic)
            pipedList.append(piped)
        return pipedList


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    main()
    _test()
