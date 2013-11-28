
v2.1
====
Minor version update.

New features
-----------
This version includes the following new features.

- webapp
    - editable comment
    - dynamically loading tables
- figure node
- document generator (using Sphinx)
- submodules in dataprocessor/
    - exception.py
    - execute.py
    - figure.py
    - io.py
    - nodes.py
    - table.py
    - utility.py

Removed
-------

The following pipes are removed.
These features are replaced by the webapp.

- generatehtml.py
- etreeio.py
- infomanager.py
- table.py (refactored to dataprocessor/table.py)

