DataProcessor
=============

A data processing library.

Sample usage is written in [here](sample/README.md "Sample Usage").

WebApp
======
You can browse your data managed with DataProcessor by a DataProcessor webapp.
In order to edit data through this webapp, a HTTP server is necessary.
This project contains a script `bin/server.py` which start/stop a simple HTTP server.
The usage of this script is also written in `sample/README.md`

Requirements
------------

- python-daemon (>= 1.6) (for stand a HTTP server as a daemon)


For Developer
=============

If you want to develop this tools, please read [Developer Guide](developer.md "Developer Guide").

Lisence
==========
GPLv3
