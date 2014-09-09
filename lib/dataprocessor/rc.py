# coding=utf-8
"""Configure manager of dataprocessor
"""

from . import utility, io
import os.path
import argparse
import ConfigParser


default_rcpath = "~/.dataprocessor.ini"


def get_run_dir(root_path):
    """Get path of dir in which run dirs are placed.

    Parameter
    ---------
    root_path: str
        path of data root

    """
    path = os.path.join(root_path, "Runs")
    return utility.get_directory(path)


def get_project_dir(root_path):
    """Get path of dir in which project dirs are placed.

    Parameter
    ---------
    root_path: str
        path of data root

    """
    path = os.path.join(root_path, "Projects")
    return utility.get_directory(path)


def get_figure_dir(root_path):
    """Get path of dir in which figure dirs are placed.

    Parameter
    ---------
    root_path: str
        path of data root

    """
    path = os.path.join(root_path, "Figures")
    return utility.get_directory(path)


def ArgumentParser(rcpath=default_rcpath):
    """Argument parser for executables in this project.

    Parameter
    ---------
    rcpath: str, optional
        path of configure file (default=~/.dataprocessor.ini)

    Return
    ------
    argparse.ArgumentParser instance

    """
    cfg = load_configure_file(rcpath)
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=cfg["root"],
                        help="data root")
    parser.add_argument("--json", default=cfg["json"],
                        help="path of data JSON")
    parser.add_argument("--debug", help="output traceback")
    return parser


def load(rcpath=default_rcpath):
    """Load node_list from default data.json.

    Parameter
    ---------
    rcpath: str, optional
        path of configure file (default=~/.dataprocessor.ini)

    Return
    ------
    node_list

    """
    cfg = load_configure_file(rcpath)
    return io.load([], cfg["json"])


def update(node_list, rcpath=default_rcpath):
    """Save node_list into default data.json with update strategy.

    Parameter
    ---------
    rcpath: str, optional
        path of configure file (default=~/.dataprocessor.ini)

    """
    cfg = load_configure_file(rcpath)
    with io.SyncDataHandler(cfg["json"], silent=True) as dh:
        dh.update(node_list)


def create_configure_file(rcpath=default_rcpath):
    """Create configure file.

    Parameter
    ---------
    rcpath: str, optional
        path of configure file (default=~/.dataprocessor.ini)

    """
    print("Creating " + rcpath)
    root = raw_input("Enter your Root direcotry: ")
    root_dir = utility.get_directory(root)
    default_path = os.path.join(root_dir, "data.json")
    json_path = raw_input("Enter path of your data json (default:{}): "
                          .format(default_path))
    if not json_path:
        json_path = default_path
    json_path = utility.path_expand(json_path)
    if not os.path.exists(json_path):
        print("Creating " + json_path)
        with open(json_path, "w") as f:
            f.write("[]")

    cfg = ConfigParser.RawConfigParser()
    cfg.add_section("data")
    cfg.set("data", "root", root_dir)
    cfg.set("data", "json", json_path)

    with open(rcpath, 'wb') as f:
        cfg.write(f)
    print("Your configure file: " + rcpath + " is successfully created")


def load_configure_file(rcpath=default_rcpath):
    """Load default configure.

    If the configure file does not exist, it will be created.
    (see `create_configure_file(rcpath)`)

    Parameter
    ---------
    rcpath: str, optional
        path of configure file (default=~/.dataprocessor.ini)

    Return
    ------
    dict
        There are two keys: "root" and "json".

    """
    rcpath = utility.path_expand(rcpath)
    if not os.path.exists(rcpath):
        print("Configure file: " + rcpath + " does not exists")
        ans = raw_input("Create now? [Y/n]")
        if ans in ["n", "N", "no", "No", "NO"]:
            return {"json": "", "root": ""}
        create_configure_file(rcpath)

    parser = ConfigParser.SafeConfigParser()
    parser.read(rcpath)
    return {
        "root": parser.get("data", "root"),
        "json": parser.get("data", "json"),
    }
