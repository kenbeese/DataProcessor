DataProcessor
=============
[![Build Status](https://travis-ci.org/kenbeese/DataProcessor.png)](https://travis-ci.org/kenbeese/DataProcessor)

A data processing library.

Data Processing
---------------
DataProcessor is a framework for managing meta data of numerical analysis.
This allows you to gather meta data of your data,
to write command to process your data, and to browse your data.

In order to read the following explaination and to use this framework,
you should be familiar with JSON format.

If you only want to use browsing feature,
you can skip to [Browsing](Browsing).

This introduces three basic concepts:

- [node](#node)
- [pipe](#pipe)
- [manipulations](#manipulations)

### node
Numerical analysis often yields huge data
which are almost same but slightly different.
We call each of these data as *run*, and series of them as *project*.
Since these runs and projects will be related each others,
we can consider a network of them.
Thus we call each of runs and projects as **node**.
We assume that each of runs and projects has a corresponding directory,
and that these directories are not duplicated.
So the identifier of node is the path of its directory.

### pipe
This framework introduces a concept **pipe**
corresponding to a single process for nodes.
Since nodes are managed with a list of node (called `node_list`),
pipe can be regarded as a single process for `node_list`.
In other words, pipes are implemented as a function
which receives `node_list` as an argument and returns processed `node_list`.
For example, 

- `save_json` pipe saves `node_list` into a JSON file.
- `load_json` pipe loads `node_list` from a JSON file.
- `scan_directory` pipe gathers runs or projects and appends it into `node_list`.
- `add_comment` pipe add comments to a specified node.
- `configure` pipe collects meta data of each run.

You can combine them to satisfy your purpose.
If you want to scan your data and save meta data into a JSON file,
the combined pipes can be written as follows:

                           +----------------+    +-----------+    +-----------+
    [node_list (empty)] => | scan_directory | => | configure | => | save_json |
                           +----------------+    +-----------+    +-----------+

As `node_list` pass through pipes, it will be modified:

1. `node_list` is empty at first
```
node_list = []
```

1. `scan_directory` gathers meta data and `node_list` becomes
```
node_list = [
    {"path": "/path/to/data1", "name": "data1", ...}, 
    {"path": "/path/to/data2", "name": "data2", ...}, 
    ...
]
```

1. `configure` appends an attribute "configure"
```
node_list = [
    {
        "path": "/path/to/data1", "name": "data1",
        "configure": {
            "N": 128,
            ...
        },
        ...
    }, 
    ...
]
```

1. `save` does not change `node_list` but saves it into a JSON file.

We call a series of pipes as **manipulations**.
The detail of pipes is documented in [pipes](doc/pipes.md).

### manipulations
You can execute **manipulations** with an executable script [bin/dataprocessor](sample/README.md#dataprocessor).
You must specify manipulations by a JSON file.
For example, the above example corresponds to the following JSON format:

```json
[
    {"name": "scan_directory", "args": ["./datadir", ["*.conf", "*.ini"]]},
    {"name": "configure", "args": ["parameters.conf"], "kwds": {}},
    {"name": "save_json", "args": ["data.json"],  "kwds": {}}
]
```

If you save this into `manip.json`,
you can do manipulations by the following command:

    $ bin/dataprocessor manip.json

Another sample is here:

    +-----------+    +-------------+    +-----------+
    | load_json | => | add_comment | => | save_json |
    +-----------+    +-------------+    +-----------+

1. load `node_list` from a JSON file `data.json`
1. write a comment in `node_list`
1. save `node_list` into the same JSON file

Corresponding JSON is following:

```json
[
    {"name": "load_json", "args": ["data.json"]},
    {"name": "add_comment", "args": ["comment comment", "/path/to/node"]},
    {"name": "save_json", "args": ["data.json"],  "kwds": {}}
]
```

Saving this JSON into `manip.json`,
this manipulations is executed by the following command:

    $ bin/dataprocessor manip.json

Most part of manipulations will be in such form;
load data, do a pipe, and save data.

However, if two `dataprocessor` run simultaneously,
there data I/O conflict:

1. process1 loads
1. process2 loads
1. process1 saves
1. process2 saves < conflict:
the JSON file is different from that when process2 read it.

In order to avoid this, synchronized I/O are provided.
Save the following JSON into a `manip_sync.json`.

```json
[
    {"name": "add_comment", "args": ["comment comment", "/path/to/node"]},
]
```
And then 

    $ bin/dataprocessor --data=data.json manip_sync.json

or

    $ bin/dataprocessor -d data.json manip_sync.json

The option `--data` or `-d` enable you to strip `load_json` and `save_json`.
In addition, the JSON file is locked:
the process started latter will wait unless the former finish.

WebApp
======
You can browse your data managed with DataProcessor by a DataProcessor webapp.
In order to edit data through this webapp, a HTTP server is necessary.
This project contains a script `bin/server.py` which start/stop a simple HTTP server.
The usage of this script is also written in [sample](sample/README.md "Sample Usage for WebApp").

Requirements
------------

- python-daemon (>= 1.6) (for stand a HTTP server as a daemon)
- jinja2 (for converting template)


For Developer
=============

If you want to develop this tools, please read [Developer Guide](doc/developer.md "Developer Guide").

Lisence
==========
GPLv3
