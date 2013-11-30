DataProcessor
=============

A data processing library.

Sample usage is written in [here](sample/README.md "Sample Usage").

Data processing procedure
-----
This library collects and processes information of run directories.

Each run directory or project, which consists of multiple run directories,
is referred to as **node**.
Using this library, you can manipulate a list of **node** via **pipe**s.
A **pipe** corresponds to a single manipulation.
For exapmle, you can add new run directories or projects, add some comments to them,
or collect information of parameters from each run directory.

dataprocessor executes a procedure, that is, a list of **pipe**s
described in the specified json file and modify a list of **node**
stored in another json file.
Details of **pipe**s is documented in [pipes list](doc/pipe.md).

You can also execute some **pipe**s via WebApp explained in the below.


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
