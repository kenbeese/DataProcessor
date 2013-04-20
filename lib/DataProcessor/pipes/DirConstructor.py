class DirConstructor(object):
    """
    IO for run_results file formatted as JSON.


    Usage:
    >>> filestring = '''[rundir]
    ... dir_prefix = run
    ... num_format = 02d
    ... #rundirname = dir_prefix + "%" + num_format
    ... #In this case, rundirname = run%02d
    ... '''
    >>> f = open("/tmp/conffile", "w")
    >>> f.write(filestring)
    >>> f.close()
    >>> import os
    >>> os.mkdir("/tmp/run02")
    >>> os.mkdir("/tmp/run03")
    >>> os.mkdir("/tmp/run004")
    >>> try:
    ...     hoge = DirConstructor("/tmp/conffile")
    ...     print hoge.listPath()
    ...     print hoge.listPath((2, 3))
    ...     print hoge.listPath((2, 3, 4))
    ...     print hoge.path2num("/tmp/run02")
    ... finally:
    ...     os.rmdir("/tmp/run02")
    ...     os.rmdir("/tmp/run03")
    ...     os.rmdir("/tmp/run004")
    ...     os.remove("/tmp/conffile")
    /tmp/run04 is not exists.
    [{'path': '/tmp/run02'}, {'path': '/tmp/run03'}]
    [{'path': '/tmp/run02'}, {'path': '/tmp/run03'}]
    /tmp/run04 is not exists.
    [{'path': '/tmp/run02'}, {'path': '/tmp/run03'}]
    2
    >>> print hoge.path2num("/tmp/run05")
    Traceback (most recent call last):
        ...
    Exception: /tmp/run05 is not exists.
    >>> print hoge.num2path(2)
    Traceback (most recent call last):
        ...
    Exception: /tmp/run02 is not exists.
    """

    def __init__(self, conf_path):
        import os.path
        from ConfigParser import SafeConfigParser
        config = SafeConfigParser()
        config.read(os.path.abspath(conf_path))
        self.conf = []
        for opt in config.options("rundir"):
            self.conf[opt] = config.get("rundir", opt)
        self.conf["topdir_path"] = os.path.abspath(os.path.dirname(conf_path))




    def listPath(self, num_list = False):
        import glob, os

        dirlist = []

        if num_list:
            for num in num_list:
                try:
                    dirlist.append(self.num2path(int(num)))
                except Exception as e:
                    print(e)

        else :
            search_str = os.path.join(self.conf["topdir_path"], self.conf["dir_prefix"]) + "[0-9]*"
            for dir in glob.glob(search_str):
                num = self.path2num(dir)
                try:
                    dirlist.append(self.num2path(num))
                except Exception as e:
                    print(e)
        return [{"path":path} for path in dirlist]


    def path2num(self, path):
        import os.path
        if (not os.path.exists(path)):
            raise Exception(path + " is not exists.")
        base = self.__path2basename(path)

        return self.__basename2num(base)


    def num2path(self, num):
        import os.path
        path = os.path.join(self.conf["topdir_path"], self.__num2basename(num))
        if (not os.path.exists(path)):
            raise Exception(path + " is not exists.")
        return path


    def __num2basename(self, num):
        return (self.conf["dir_prefix"] + "%" + self.conf["num_format"]) % int(num)


    def __basename2num(self, dirname):
        return int(dirname.lstrip(self.conf["dir_prefix"]))


    def __path2basename(self, path):
        import os.path
        return os.path.basename(os.path.normpath(path))



def runPaths(run_list, conf):
    DC = DirConstructor(conf)
    run_list = run_list + DC.listPath()
    return run_list


def register(inputs_dics):
    inputs_dics["runnum"] = {
        "func": runPaths,
        "args": ["conf"],
        "desc": "read runs configure and output runs dir paths"
        }



def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
