# -*- coding: utf-8 -*-

import os
import json
import urllib2
import BaseHTTPServer
import CGIHTTPServer
from daemon import DaemonContext
from daemon.pidfile import PIDLockFile

from . import utility
from . import exception


def start(args):
    port = int(args.port)
    root_dir = utility.check_directory(args.root)
    log_path = os.path.join(root_dir, args.logfile)
    lock_path = args.lockfile

    data_path = utility.check_file(args.json)
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
        raise exception.DataProcessorError("Server already stands.")


def stop(args):
    lock_path = args.lockfile
    if os.path.exists(lock_path):
        pid = int(open(lock_path, 'r').read())
        os.kill(pid, 15)
        os.remove(lock_path)
    else:
        raise exception.DataProcessorError("Server does not stand")


def install(args):
    """Install jQuery."""
    root_dir = utility.check_directory(args.root)
    dest_path = os.path.join(root_dir, "js")

    jquery_filename = "jquery-1.10.2.js"
    jquery_url = "http://code.jquery.com/" + jquery_filename
    with open(os.path.join(dest_path, jquery_filename), "w") as f:
        f.write(urllib2.urlopen(jquery_url).read())

    jquery_cookie_filename = "jquery.cookie.js"
    jquery_cookie_url = "https://raw.github.com/carhartl/jquery-cookie/master/src/"\
        + jquery_cookie_filename
    with open(os.path.join(dest_path, jquery_cookie_filename), "w") as f:
        f.write(urllib2.urlopen(jquery_cookie_url).read())
