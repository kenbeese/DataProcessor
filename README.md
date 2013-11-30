DataProcessor
=============

A data processing library.

Data processing
-----
This library collects and processes information of "run"s.

### node
If you are a physicist or a computer scientist,
you may have huge data which are almost same but slightly different.
We call each of these data as "run",
and series of them as "project".
Since these runs and projects will be related each others,
we can consider a network of them.
Thus we call each of runs and projects as **node**.
We assume that each of runs and projects has their directory,
and the path of the directory is unique.
So the identifier of **node** is the path of its directory.

### pipe
This library introduce **pipe** corresponding to a single manipulation for **node**s;
since this library manages nodes by a list of node (called **node_list**),
**pipe** do a single manipulation for **node_list**.
For exapmle, 

- "scan" pipe gathers runs or projects and appends it into the node_list,
- "add_comment" pipe add some comments to a specified node
- "configure" pipe collects information of parameters from each run directory.

You can easily combine them to satisfy your purpose.
We call combined pipes as **manipulations**, and specified in JSON format.
Details of **pipe**s is documented in [pipes list](doc/pipe.md).


### manipulations
The executable script `bin/dataprocessor` executes a procedure, that is, a list of **pipe**s
described in the specified json file and modify a list of **node**
stored in another json file.
You can also execute some **pipe**s via WebApp explained in the below.
Sample usage is written in [here](sample/README.md "Sample Usage").

WebApp
======
You can browse your data managed with DataProcessor by a DataProcessor webapp.
In order to edit data through this webapp, a HTTP server is necessary.
This project contains a script `bin/server.py` which start/stop a simple HTTP server.
The usage of this script is also written in [sample](sample/README.md "Sample Usage for WebApp").

Requirements
------------

- python-daemon (>= 1.6) (for stand a HTTP server as a daemon)


For Developer
=============

If you want to develop this tools, please read [Developer Guide](doc/developer.md "Developer Guide").

Lisence
==========
GPLv3
