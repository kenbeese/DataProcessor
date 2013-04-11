# coding=utf-8

import json

def dump(run_list):
    """
    dump run_list as JSON string

    >>> run_list = [
    ...     {'path': '/tmp/run01',
    ...     'meta': {'comment': 'come', 'date': '1989/03/12 12:24',
    ...         'optional': None,
    ...         'tags': ['tag1', 'tag3']},
    ...     'configure':{'conf1':'3', 'conf2': '4', 'conf4': '2', 'conf5': '5'},
    ...     },
    ...     {'path': '/tmp/run02',
    ...     'meta': {'comment': 'come', 'date': '1989/03/12 12:24',
    ...         'optional': None,
    ...         'tags': ['tag1', 'tag3']},
    ...     }]
    >>> dump(run_list) == '[{"path": "/tmp/run01", "meta": {"comment": "come", "date": "1989/03/12 12:24", "optional": null, "tags": ["tag1", "tag3"]}, "configure": {"conf2": "4", "conf1": "3", "conf5": "5", "conf4": "2"}}]'
    True
    """
    valid_run_list = [run for run in run_list if "path" in run and "meta" in run and "configure" in run]
    return json.dumps(valid_run_list)

def register(pipes_dics):
    pipes_dics["output_json"] = {
        "func" : dump,
        "args" : [],
        "desc" : "dump valid runs into JSON string"
        }

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
