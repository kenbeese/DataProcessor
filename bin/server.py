#!/usr/bin/env python
# coding=utf-8
"""Start/Stop a simple HTTP server."""

import os
import os.path
import sys
import json
import argparse
import urllib2
import BaseHTTPServer
import CGIHTTPServer
from daemon import DaemonContext
from daemon.pidfile import PIDLockFile

sys.path = ([sys.path[0]]
            + [os.path.join(os.path.dirname(__file__), "../lib")]
            + sys.path[1:])
import dataprocessor as dp
sys.path = [sys.path[0]] + sys.path[2:]


def start(args):
    port = int(args.port)
    root_dir = dp.utility.check_directory(args.root)
    log_path = os.path.join(root_dir, args.logfile)
    lock_path = args.lockfile

    data_path = dp.utility.check_file(args.data_json)
    cfg = {"data_path": data_path}
    with open(os.path.join(root_dir, "cfg.json"), 'w') as f:
        json.dump(cfg, f)

    if not os.path.exists(lock_path):
        dc = DaemonContext(pidfile=PIDLockFile(lock_path),
                           stderr=open(log_path, "w+"),
                           working_directory=root_dir)
        with dc:
            server = BaseHTTPServer.HTTPServer
            handler = CGIHTTPServer.CGIHTTPRequestHandler
            addr = ("", port)
            # handler.cgi_directories = [""]
            httpd = server(addr, handler)
            httpd.serve_forever()
    else:
        raise dp.exception.DataProcessorError("Server already stands.")


def stop(args):
    lock_path = args.lockfile
    if os.path.exists(lock_path):
        pid = int(open(lock_path, 'r').read())
        os.kill(pid, 15)
        os.remove(lock_path)
    else:
        raise dp.exception.DataProcessorError("Server does not stand")


def install(args):
    """Install jQuery."""
    root_dir = dp.utility.check_directory(args.root)
    dest_path = os.path.join(root_dir, "js")

    jquery_filename = "jquery-1.10.2.js"
    jquery_url = "http://code.jquery.com/" + jquery_filename
    with open(os.path.join(dest_path, jquery_filename), "w") as f:
        f.write(urllib2.urlopen(jquery_url).read())

    jquery_cookie_filename = "jquery.cookie.js"
    jquery_cookie_url = "https://raw.github.com/carhartl/jquery-cookie/master/" + jquery_cookie_filename
    with open(os.path.join(dest_path, jquery_cookie_filename), "w") as f:
        f.write(urllib2.urlopen(jquery_cookie_url).read())


def main():
    parser = argparse.ArgumentParser()
    sub_psr = parser.add_subparsers()

    # start
    start_psr = sub_psr.add_parser("start", help="start articles daemon")
    start_psr.set_defaults(func=start)
    start_psr.add_argument("data_json",
                           help="A path to JSON file in which data is saved.")
    start_psr.add_argument("-p", "--port", default=8080,
                           help="Port for the server (default=8080)")
    start_psr.add_argument("--root",
                           default=os.path.join(os.path.dirname(__file__),
                                                "../server"),
                           help="""The root dir where the server stands
                                   (default=${PROJECT_HOME}/server)""")
    start_psr.add_argument("--logfile", default="server.log",
                           help="The name of the log file")
    start_psr.add_argument("--lockfile", default="/tmp/DataProcessorServer.pid",
                           help="Lock filename")

    # stop
    stop_psr = sub_psr.add_parser("stop", help="kill articles server")
    stop_psr.add_argument("--lockfile", default="/tmp/DataProcessorServer.pid",
                           help="Lock filename")
    stop_psr.set_defaults(func=stop)

    # install
    install_psr = sub_psr.add_parser("install", help="install jQuery")
    install_psr.set_defaults(func=install)
    install_psr.add_argument("--root",
                             default=os.path.join(os.path.dirname(__file__),
                                                  "../server"),
                             help="""The root dir where the server stands
                                   (default=${PROJECT_HOME}/server)""")

    # call
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    try:
        main()
    except dp.exception.DataProcessorError as e:
        print("ERROR: %s" % e.msg)
        sys.exit(1)
