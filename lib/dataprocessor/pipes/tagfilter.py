def filter(run_list, *tags):
    """
    >>> run_list = [{"path":"hoge", "meta":{"tags":["tag1", "tag2"]}},
    ...     {"path":"hoge2", "meta":{"tags":["tag1", "tag4"]}},
    ...     {"path":"hoge3", "meta":{"tags":["tag2", "tag2"]}},
    ...     {"path":"hoge4", "meta":{"tags":["tag12", "tag3"]}},
    ...     {"path":"hoge5", "meta":{"tags":["tag1", "tag2"]}}]
    >>> filter(run_list, "tag1") == [
    ...     {'path':'hoge', 'meta':{'tags':['tag1', 'tag2']}},
    ...     {'path':'hoge2', 'meta':{'tags':['tag1', 'tag4']}},
    ...     {'path':'hoge5', 'meta':{'tags':['tag1', 'tag2']}}]
    True
    >>> filter(run_list, "tag1", "tag2") == [
    ...     {'path':'hoge', 'meta':{'tags':['tag1', 'tag2']}},
    ...     {'path':'hoge5', 'meta':{'tags':['tag1', 'tag2']}}]
    True
    """
    if (len(tags) == 1):
        return [run for run in run_list if tags[0] in run["meta"]["tags"]]
    else:
        filtered = [run for run in run_list if tags[0] in run["meta"]["tags"]]
        filtered = filter(filtered, *tags[1:])
    return filtered


def register(pipes_dics):
    pipes_dics["tagFilter"] = {
        "func" : filter,
        "args" : ["tag"],
        "desc" : "extract run with tag"
        }


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
