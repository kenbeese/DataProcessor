#!/usr/bin/python
# coding=utf-8

import os
import os.path
import sys
import argparse
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
    lock_path = "/tmp/DataProcessorServer.pid"

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
    lock_path = "/tmp/DataProcessorServer.pid"
    if os.path.exists(lock_path):
        pid = int(open(lock_path, 'r').read())
        os.kill(pid, 15)
        os.remove(lock_path)
    else:
        raise dp.exception.DataProcessorError("Server does not stand")


def main():
    parser = argparse.ArgumentParser()
    sub_psr = parser.add_subparsers()
    start_psr = sub_psr.add_parser("start", help="start articles daemon")
    start_psr.set_defaults(func=start)
    start_psr.add_argument("port", help="Port for the server")
    start_psr.add_argument("root", help="The root dir where the server stands")
    start_psr.add_argument("--logfile", default="server.log",
                           help="The name of the log file (generated in root dir)")
    sub_psr.add_parser("stop",help="kill articles server").set_defaults(func=stop)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    try:
        main()
    except dp.exception.DataProcessorError as e:
        print("ERROR: %s" % e.msg)
        sys.exit(1)
