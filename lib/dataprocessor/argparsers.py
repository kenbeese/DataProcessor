# coding=utf-8
import argparse
import sys
import os

from . import pipes
from . import rc
from . import server


def dpmanip():
    try:
        parser = rc.ArgumentParser()
    except rc.DataProcessorRcError:
        print("Please create configure file by dpinit")
        sys.exit(1)

    parser.add_argument("-s", "--silent", action="store_true",
                        help="Does not ask whether REPLACE JSON file")
    parser.add_argument("-i", "--input", action="store_true",
                        help="Use stdin as data JSON")
    parser.add_argument("-o", "--output", action="store_true",
                        help="Output result node_list")
    parser.add_argument("-r", "--replace", action="store_true",
                        help="Use replace strategy for saving JSON")
    sub_psr = parser.add_subparsers(title="subcommands", metavar="pipes")
    for name, val in pipes.pipes_dics.items():
        pipe_psr = sub_psr.add_parser(name, help=val["desc"])
        for name, attr in val["args"]:
            pipe_psr.add_argument(name, **attr)
        if "kwds" in val:
            for kwd, attr in val["kwds"]:
                pipe_psr.add_argument("--" + kwd, **attr)
        pipe_psr.set_defaults(val=val)
    return parser


def dpgenzshcomp():
    parser = argparse.ArgumentParser()
    executable_names = [
        "dpmanip",
        "dpgenzshcomp",
        "dataprocessor",
        "register_figure",
        "dpserver"
    ]
    parser.add_argument("EXECUTABLE", choices=executable_names)
    return parser


def dataprocessor():
    parser = argparse.ArgumentParser(description="""
                command line interface for DataProcessor pipeline""")
    parser.add_argument('manip_json')
    parser.add_argument(
        '-d', "--data", nargs="?", help="The path of data JSON")
    return parser


def dpserver():
    parser = rc.ArgumentParser()
    sub_psr = parser.add_subparsers()

    port_cfg = {
        "default": 8080,
        "help": "Port for the server"
    }
    root_cfg = {
        "default": os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                "../../server")),
        "help": "The root dir where the server stands"
    }
    logfile_cfg = {
        "default": "server.log",
        "help": "The name of the log file",
    }
    lockfile_cfg = {
        "default": "/tmp/DataProcessorServer.pid",
        "help": "Lock filename",
    }

    # start
    start_psr = sub_psr.add_parser("start",
                                   help="start DataProcessor server daemon")
    start_psr.set_defaults(func=server.start)
    rc.load_into_argparse(start_psr, "dpserver", {
        "port": port_cfg,
        "root": root_cfg,
        "logfile": logfile_cfg,
        "lockfile": lockfile_cfg,
    }, allow_empty=True)

    # stop
    stop_psr = sub_psr.add_parser("stop", help="kill articles server")
    stop_psr.set_defaults(func=server.stop)
    rc.load_into_argparse(stop_psr, "dpserver", {
        "lockfile": lockfile_cfg,
    }, allow_empty=True)

    # install
    install_psr = sub_psr.add_parser("install", help="install jQuery")
    install_psr.set_defaults(func=server.install)
    rc.load_into_argparse(install_psr, "dpserver", {
        "root": root_cfg,
    }, allow_empty=True)
    return parser


def register_figure():
    parser = argparse.ArgumentParser(description="""
                Register generated figures into DataProcessor.
                The options -R and -g must be specified after ususal arguments.
                """)
    parser.add_argument("figure_directory",
                        help="The directory for saving figures")
    parser.add_argument("json_file",
                        help="The path of JSON file containing nodes")
    parser.add_argument("figures", nargs="+",
                        help="Paths of the figures that you want to register")
    parser.add_argument("-R", "--runs", dest="runs", nargs="+",
                        help="Paths of runs related to figures")
    parser.add_argument("-g", "--generators", dest="generators",
                        nargs="+", default=[],
                        help="Paths of generator files (s.t. fig.gp, fig.py)")
    return parser
