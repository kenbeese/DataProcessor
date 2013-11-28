DataProcessor
=============

A data processing library.

Sample usage is written in `sample/README.md`

WebApp
======
You can browse your data managed with DataProcessor by a DataProcessor webapp.
In order to edit data through this webapp, a HTTP server is necessary.
This project contains a script `bin/server.py` which start/stop a simple HTTP server.
The usage of this script is also written in `sample/README.md`

Requirements
------------

- python-daemon (>= 1.6) (for stand a HTTP server as a daemon)


Build HTML documents
====================
Requirements
------------
- sphinx (python documentation tools)
- numpydoc (Sphinx extention)

If you have not installed these,

    # easy_install sphinx numpydoc

Build
-----
After installation of above library,
you can make api reference of this library with following command.

    $ make -C doc html

The file `doc/_build/html/index.html` is top page.


Lisence
==========
GPLv3
