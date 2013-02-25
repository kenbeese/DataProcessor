from ConfigParser import SafeConfigParser


class ConfManager(SafeConfigParser):
    """
    """
    def __init__(self):
        SafeConfigParser.__init__(self)
        self.optionxform = str



    def confDict(self, section = None):
        """
        if SECTION is None, return all configure.

        >>> filestring = '''[sec1]
        ... conf1 = 3
        ... conf2 = 4
        ... [sec2]
        ... conf4 = 2
        ... conf1 = 5
        ... '''
        >>> f = open("/tmp/testfile", "w")
        >>> f.write(filestring)
        >>> f.close()
        >>> cm = ConfManager()
        >>> cm.read("/tmp/testfile")
        ['/tmp/testfile']
        >>> sec1 = cm.confDict("sec1")
        >>> sec2 = cm.confDict("sec2")
        >>> print sec1['conf1']
        3
        >>> print sec1['conf2']
        4
        >>> print sec2['conf1']
        5
        >>> print sec2['conf4']
        2
        >>> import os
        >>> os.remove("/tmp/testfile")
        """
        if section == None:
            seclist = self.sections()
        else:
            seclist = [section]

        conf_d = {}
        for sec in seclist:
            for key in self.__keylist(sec):
                conf_d[key] = self.get(sec, key)
        return conf_d


    def __keylist(self, sec):
        key_var_list_ = self.items(sec)
        keylist_ = []
        for key, var in key_var_list_:
            keylist_.append(key)
        return keylist_


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
