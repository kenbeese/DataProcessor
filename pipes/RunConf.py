def add(run_list, runs_conf_path):
    """
    Add configure dictionary to run_list

    Usage:

    >>> import os
    >>> os.mkdir("/tmp/run01/")
    >>> os.mkdir("/tmp/run02/")
    >>> filestring = '''[sec1]
    ... conf1 = 3
    ... conf2 = 4
    ... [sec2]
    ... conf4 = 2
    ... conf5 = 5
    ... '''
    >>> f = open("/tmp/run01/para.conf", "w")
    >>> f.write(filestring)
    >>> f.close()
    >>> filestring = '''[sec1]
    ... conf1 = 21
    ... conf2 = 1
    ... [sec2]
    ... conf4 = 3.23
    ... conf5 = 42
    ... '''
    >>> f = open("/tmp/run02/para.conf", "w")
    >>> f.write(filestring)
    >>> f.close()
    >>> filestring = '''[rundir]
    ... conf_name = para.conf
    ... '''
    >>> f = open("/tmp/runs.conf", "w")
    >>> f.write(filestring)
    >>> f.close()
    >>> run_list = [{"path":"/tmp/run02"}, {"path":"/tmp/run01"}]
    >>> add(run_list, "/tmp/runs.conf") == [
    ...     {'path':'/tmp/run02',
    ...     'configure':{'conf1':'21', 'conf2': '1', 'conf4': '3.23', 'conf5': '42'}},
    ...     {'path':'/tmp/run01',
    ...     'configure':{'conf1':'3', 'conf2': '4', 'conf4': '2', 'conf5': '5'}}]
    True
    >>> os.remove("/tmp/run01/para.conf")
    >>> os.remove("/tmp/run02/para.conf")
    >>> os.rmdir("/tmp/run01/")
    >>> os.rmdir("/tmp/run02/")
    """

    import os.path
    from ..libs.ConfManager import ConfManager

    confkey = "configure"

    runs_parser = ConfManager()
    runs_parser.read(os.path.abspath(runs_conf_path))
    confname = runs_parser.get("rundir", "conf_name")

    L = []
    for run in run_list:
        path = os.path.join(run["path"], confname)
        parser = ConfManager()
        parser.read(path)
        confdic = parser.confDict()
        confdic = {confkey:confdic}
        confdic.update(run)
        L.append(confdic)

    run_list = L
    return run_list



def register(pipes_dics):
    pipes_dics["configure"] = {
        "func" : add,
        "args" : ["runs_conf_path"],
        "desc" : "add run cofigure"
        }


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
