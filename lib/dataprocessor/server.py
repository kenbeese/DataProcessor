# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import os.path as op
import json
import urllib2
import BaseHTTPServer
import CGIHTTPServer
from zipfile import ZipFile
from tempfile import NamedTemporaryFile
from daemon import DaemonContext
from daemon.pidfile import PIDLockFile

from . import utility
from . import exception


def start(args):
    port = int(args.port)
    root_dir = utility.check_directory(args.root)
    log_path = op.join(root_dir, args.logfile)
    lock_path = args.lockfile

    data_path = utility.check_file(args.json)
    cfg = {"data_path": data_path}
    with open(op.join(root_dir, "cfg.json"), 'w') as f:
        json.dump(cfg, f)

    if not op.exists(lock_path):
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
    if op.exists(lock_path):
        pid = int(open(lock_path, 'r').read())
        os.kill(pid, 15)
        os.remove(lock_path)
    else:
        raise exception.DataProcessorError("Server does not stand")


def install(args):
    """Install jQuery and Bootstrap.
    """
    root_dir = utility.check_directory(args.root)
    jspath = op.join(root_dir, "js")
    csspath = op.join(root_dir, "css")

    jquery_filename = "jquery-1.10.2.js"
    jquery_url = "http://code.jquery.com/" + jquery_filename
    print("Downloading jQuery...", end="")
    with open(op.join(jspath, jquery_filename), "w") as f:
        f.write(urllib2.urlopen(jquery_url).read())
    print("Done.")

    jquery_cookie_filename = "jquery.cookie.js"
    jquery_cookie_url = "https://raw.github.com/carhartl/jquery-cookie/master/src/"\
        + jquery_cookie_filename
    print("Downloading jQuery Cookie...", end="")
    with open(op.join(jspath, jquery_cookie_filename), "w") as f:
        f.write(urllib2.urlopen(jquery_cookie_url).read())
    print("Done.")

    bootstrap_version = "3.3.1"
    bootstrap_url = "https://github.com/twbs/bootstrap/releases/download/"\
        + "v{version}/bootstrap-{version}-dist.zip"\
        .format(version=bootstrap_version)
    print("Downloading Bootstrap...", end="")
    with NamedTemporaryFile(suffix=".zip", delete=False) as f:
        bootstrap_name = f.name
        f.write(urllib2.urlopen(bootstrap_url).read())

    def _copy_file(path, fn):
        with zf.open(fn) as f_from:
            with open(op.join(path, op.basename(fn)), 'w') as f_to:
                f_to.write(f_from.read())

    with ZipFile(bootstrap_name, 'r') as zf:
        _copy_file(jspath, "dist/js/bootstrap.min.js")
        _copy_file(csspath, "dist/css/bootstrap.min.css")
    print("Done.")
