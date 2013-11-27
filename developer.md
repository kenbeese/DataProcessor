
server API reference
====================

manip
-----

Do a manipulation on server.

### address
`/cgi-bin/api.cgi`

### Request
```
"type" : "manip"
"manip" : json_str
```

### Response
JSON will be returned.

If the manipulation succeed:
```json
{
    "exit_code" : 0
}
```
If the manipulation fails:
```json
{
    "exit_code" : exit_code,
    "message" : error_message
}
```
See also `handler.operation_sucess` and `handler.operation_fail`.

pipe
----

Do a manipulation s.t. [load, pipe, save].

### address
`/cgi-bin/api.cgi`

### Request
```
"type" : "pipe",
"name" : name_of_pipe,
"args" : args_json, # list 
"kwds" : kwds_json  # dict, optional
```

This will create a manipulation s.t.
```
[
    {"name": "load_json", "args", ["data.json"]},
    {"name": "name_of_pipe", "args": json.loads(args_json), "kwds": json.loads(kwds_json)},
    {"name": "save_json", "args", ["data.json"], "kwds" : {"silent" : "True"}},
]
```

### Response
JSON will be returned (same as `manip`).

Projects
--------

Widgets
-------

