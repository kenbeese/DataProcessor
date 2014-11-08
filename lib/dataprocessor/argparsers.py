# coding=utf-8
import argparse
import sys

from . import pipes
from . import rc


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
        for arg in val["args"]:
            pipe_psr.add_argument(arg)
        if "kwds" in val:
            for kwd in val["kwds"]:
                pipe_psr.add_argument("--" + kwd)
        pipe_psr.set_defaults(val=val)
    return parser


def genzshcomp():
    parser = argparse.ArgumentParser()
    executable_names = [
        "dpmanip", "genzshcomp", "dataprocessor", "register_figure"]
    parser.add_argument("EXECUTABLE", choices=executable_names)
    return parser


def dataprocessor():
    parser = argparse.ArgumentParser(description="""
                command line interface for DataProcessor pipeline""")
    parser.add_argument('manip_json')
    parser.add_argument(
        '-d', "--data", nargs="?", help="The path of data JSON")
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
