
pipes
=====
- [add_comment](#add_comment)
- [configure](#configure)
- [configure_no_section](#configure_no_section)
- [load_json](#load_json)
- [register_figure](#register_figure)
- [save_json](#save_json)
- [scan_directory](#scan_directory)

add_comment
----
add comment to node with path

### args
1. **comment**
2. **path**

### kwds
None

### docstring

    Add comment to node spedcified path.

    Parameters
    ----------
    comment: str
           comment.

    node_path: str
        This path specify the unique node.

    Examples
    --------
    >>> node_list = [{"path": "/path/to/hoge"},
    ...              {"path": "/path/to/hogehoge"}]
    >>> add(node_list, "some comments", "/path/to/hoge") == [
    ...     {"path": "/path/to/hoge", "comment": "some comments"},
    ...     {"path": "/path/to/hogehoge"}]
    True
    >>> add(node_list, "some comments aho", "/path/to/hogehoge/")
    Traceback (most recent call last):
        ...
    Warning: There is no node with specified path. path = /path/to/hogehoge/
    

[top](#pipes)

---------------------

configure
----
Read parameter file (use ConfigParser)

### args
1. **filename**

### kwds
- **section**

### docstring

    Add configure to node_list.

    Parameters
    ----------
    filename : str
        filename of parameter configure file
        If file is not exists, add null list.

    section : str
        Specify section name in configure file.

    Returns
    -------
    list
        node_list which is a list of dict.

    Examples
    --------
    >>> add(node_list, "configure.conf")
    >>> # Change load section.
    >>> add(node_list, "configure.conf", "defaults")

    

[top](#pipes)

---------------------

configure_no_section
----
Read parameter file (without section)

### args
1. **filename**

### kwds
- **split_char**
- **comment_char**

### docstring

    Add configure to node_list.

    Parameters
    ----------
    filename : str
        filename of parameter configure file
        If file is not exists, add null list.
    split_char : str
        Specify the deliminator char.
    comment_char : str
        Specify the comment line signal char.

    Returns
    -------
    list
        node_list which is a list of dict.

    Examples
    --------
    >>> no_section(node_list, "foo.conf")
    >>> # Change deliminator and comment line signal
    >>> no_section(node_list, "foo.conf", split_char=":", comment_char="!")

    

[top](#pipes)

---------------------

load_json
----
load node_list from a JSON file

### args
1. **json_path**

### kwds
None

### docstring
Load node_list from a JSON file.

    Parameters
    ----------
    json_path : str
        the path to JSON

    Returns
    -------
    list
        node_list(arg1) + [new node list]

    Raises
    ------
    DataProcessorError
        occurs when JSON file does not exist.

    

[top](#pipes)

---------------------

register_figure
----
add figure node into node_list

### args
1. **figures**
2. **figure_directory**

### kwds
- **runs**
- **generators**

### docstring
 Register figure into `node_list`.

    Parameters
    ----------
    node_list : list
        node_list
    figures : list
        the present paths of figures
    figure_directory : str
        the base directory where figures are saved
    runs : list
        The paths of runs related to these figures.
        They will be saved into node["parents"]
    generators : list
        the paths of files which should be managed with the figure;
        s.t. gunplot file, python script, etc...

    

[top](#pipes)

---------------------

save_json
----
save node_list in a JSON file

### args
1. **json_path**

### kwds
- **silent**

### docstring
Save node_list into a JSON file.

    Parameters
    ----------
    json_path : str
        the path to JSON
    slient : bool, str, optional
        Ask whether replace JSON file (default=False)

    Returns
    -------
    list : node_list

    

[top](#pipes)

---------------------

scan_directory
----
Scan nodes from all directories under the directory 'root'.

### args
1. **root**
2. **whitelist**

### kwds
- **followlinks**

### docstring
Scan nodes from all directories under the directory 'root'.

    If one directory has properties of both of 'run' and 'project',
    type of the directory is set to 'run'.

    Parameters
    ----------
    root : str
        Scan directories recursively under the directory `root`.
    whitelist : list of str
        Run node has one or more file or directory
        which satisfies run_node_dir/`whitelist`.
        And project nodes satisfy project_dir/run_node_dir/`whitelist`.
        str can be specified by wildcard.
    followlinks : {'False', 'True'}, optional
        Whether scan in symbolic link.
        Be aware that setting this to True may lead to infinite recursion.

    Examples
    --------
    Initialize node_list.
    >>> node_list = directory([], "scandir_path", ["data/hoge*", "*foo*"])

    Rescan node_list.
    >>> node_list = [
    ...     {'path': '/tmp/scan_dir/run0',
    ...      'parents': [],   # empty
    ...      'children': [],  # empty
    ...      'name': 'run0',
    ...      'type': 'run'}]
    >>> node_list = directory([], "scandir_path", ["*.conf"])

    

[top](#pipes)

---------------------