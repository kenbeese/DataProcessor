Pipes
=====

- [add_comment](#add_comment)
- [configure](#configure)
- [scan_directory](#scan_directory)

add_comment
----------

Add a comment to node.

### args

1. **comment**
1. **node_path**

### kwds
None

configure
---------

Read parameter file. i.e. a node
```json
{
    "path" : "/path/to/data",
}
```
will become as follows:
```json
{
    "path" : "/path/to/data",
    "configure" : {
        "a" : "1.2",
        "val1" : "aaa"
        }
}
```


The configure file should be in `.ini` format:

```
[default]
a = 1.2
val1 = "aaa"

[section1]
b = 2.1
```

### args

1. **filename** : name of configure file

If you set `configure.ini` for this argument,
the configure file placed in `/path/to/data/configure.ini` will be load.

### kwds

- **section** (default: "parameters")  
You must specify section such as `default` or `section1` in above case.

scan_directory
--------------

Scan directories and gather basic data.
This pipe walk around directories under `root_path` and cache them.
This also introduce types of directories: "project" and "run".

### args

1. **root_path** : path of root directory from which scan start
1. **white_list** : A list of file names.  

### kwds
None
