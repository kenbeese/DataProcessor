Including directory and files
--------------

- README: This file
- manip1.json: sample json file for dataprocessor
- datadir: sample dirctory for dataprocessor
  - datadir/project1/run01/parameters.conf: run parameter file
  - datadir/project1/run03/parameters.conf: run parameter file
  - datadir/project2/run01/parameters.ini: run parameter file
  - datadir/project2/run02/parameters.ini: run parameter file
  - datadir/project2/run03/parameters.conf: run parameter file


Usage (Supposed that current directory is the same as this file)
--------
Create json file of mete information "data\_information.json".
> $ ../bin/dataprocessor ./manip1.json

Create html file from data\_information.json.
> $ ../bin/dataprocessor ./manip2.json  # Read meta information and transform html

Read data\_information.json and add configure and save to newdata.json
> $ ../bin/dataprocessor ./manip3.json

Read data\_information.json and add comment and save to newdata.json
Please change "/path/to/node" in "manip4.json" such as "${PWD}/datadir/project1/run01".
> $ ../bin/dataprocessor ./manip4.json

Add figure node
> $ ../bin/regist_figure ./figures ./data_information.json datadir/project1/run01/fig1.png
