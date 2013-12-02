DataProcessor
=============

A data processing library.

Data processing
-----
This library collects and processes information of "run"s.

### node
If you are a scientist,
you may have huge data which are almost same but slightly different.
We call each of these data as "run",
and series of them as "project".
Since these runs and projects will be related each others,
we can consider a network of them.
Thus we call each of runs and projects as **node**.
We assume that each of runs and projects has their directory,
and the path of the directory is unique.
So the identifier of **node** is the path of its directory.
In this library **node** denotes *meta data* for each run or project.
Typically, **node** contains path, name, and paths of connected nodes.

### pipe
This library introduce **pipe** corresponding to a single manipulation for **node**s;
since this library manages nodes by a list of node (called **node_list**),
**pipe** do a single manipulation for **node_list**.
For example, 

- "scan_directory" pipe gathers runs or projects and appends it into the node_list.
- "add_comment" pipe add some comments to a specified node.
- "configure" pipe collects information of parameters from each run directory.

You can easily combine them to satisfy your purpose.
We call combined pipes as **manipulations**, and specified in JSON format.
Details of **pipe**s is documented in [pipes list](doc/pipes.md).


### manipulations
You can execute **manipulations** with an executable script [bin/dataprocessor](sample/README.md#dataprocessor).
You must specify manipulations by a JSON file.
When it is written in `manipulations.json`, you can do manipulations by the following command:

    $ bin/dataprocessor manipulations.json

The following JSON executes first **pipe-name1**, next **pipe-name2**.
The **pipe**'s arguments are specified in **args** key.(**THE ORDER OF ARGS IS IMPORTANT**)
The **pipe**'s optional arguments(keywords) are specified in **kwds** key.
Currently supported **pipe** are listed in [here](doc/pipes.md).

```json
[
    {"name": "pipe-name1", "args": ["argument1", "argument2"], "kwds": {"keywords1": "some-value"}},
    {"name": "pipe-name2", "args": ["argument1"]}
]
```
This JSON file is in `sample` dir.

If you add a comment in node_list, you should want to save it.
We recommend that you save it by JSON format.
There exist JSON saver and loader pipes.

WebApp
======
You can browse your data managed with DataProcessor by a DataProcessor webapp.
In order to edit data through this webapp, a HTTP server is necessary.
This project contains a script `bin/server.py` which start/stop a simple HTTP server.
The usage of this script is also written in [sample](sample/README.md "Sample Usage for WebApp").

Requirements
------------

- python-daemon (>= 1.6) (for stand a HTTP server as a daemon)
- jinja2 (for convering template)


For Developer
=============

If you want to develop this tools, please read [Developer Guide](doc/developer.md "Developer Guide").

Lisence
==========
GPLv3
