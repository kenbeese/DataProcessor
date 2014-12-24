# -*- coding: utf-8 -*-

import os
import sys
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
    imagepath = op.join(root_dir, "images")
    if not os.path.exists(imagepath):
        os.mkdir(imagepath)

    _install_jquery(jspath)
    _install_jquery_cookie(jspath)
    _install_jquery_blockUI(jspath)
    _install_jquery_datatables(jspath, csspath, imagepath)
    _install_bootstrap(jspath, csspath)


def _install_jquery(jspath):
    jquery_filename = "jquery-1.10.2.js"
    jquery_url = "http://code.jquery.com/" + jquery_filename
    sys.stdout.write("Downloading jQuery...")
    sys.stdout.flush()
    with open(op.join(jspath, jquery_filename), "w") as f:
        f.write(urllib2.urlopen(jquery_url).read())
    print("Done.")


def _install_jquery_cookie(jspath):
    jquery_cookie_filename = "jquery.cookie.js"
    jquery_cookie_url = "https://raw.github.com/carhartl/jquery-cookie/master/src/"\
        + jquery_cookie_filename
    sys.stdout.write("Downloading jQuery Cookie...")
    sys.stdout.flush()
    with open(op.join(jspath, jquery_cookie_filename), "w") as f:
        f.write(urllib2.urlopen(jquery_cookie_url).read())
    print("Done.")


def _install_jquery_blockUI(jspath):
    jquery_blockUI_filename = "jquery.blockUI.js"
    jquery_blockUI_url = "http://malsup.github.io/" + jquery_blockUI_filename
    sys.stdout.write("Downloading jQuery blockUI...")
    sys.stdout.flush()
    with open(op.join(jspath, jquery_blockUI_filename), "w") as f:
        f.write(urllib2.urlopen(jquery_blockUI_url).read())
    print("Done.")


def _install_jquery_datatables(jspath, csspath, imagepath):

    version = "1.10.4"
    topdir = "DataTables-{}".format(version)
    url = "http://datatables.net/releases/{}.zip".format(topdir)

    sys.stdout.write("Downloading jQuery datatables...")
    sys.stdout.flush()
    req = urllib2.Request(url,
                          headers={'User-Agent': "Magic Browser"})
    with NamedTemporaryFile(suffix=".zip", delete=False) as f:
        zipname = f.name
        f.write(urllib2.urlopen(req).read())

    with ZipFile(zipname, 'r') as zf:
        _copy_file(jspath, zf,
                   topdir + "/media/js/jquery.dataTables.min.js")
        _copy_file(csspath, zf,
                   topdir + "/media/css/jquery.dataTables.css")
        for name in zf.namelist():
            if not name.find("media/images") is -1 and not name.endswith("/"):
                _copy_file(imagepath, zf, name)

        _copy_file(jspath, zf,
                   topdir + "/extensions/ColReorder/js/dataTables.colReorder.min.js")
        _copy_file(csspath, zf,
                   topdir + "/extensions/ColReorder/css/dataTables.colReorder.min.css")
        _copy_file(imagepath, zf,
                   topdir + "/extensions/ColReorder/images/insert.png")

        _copy_file(jspath, zf,
                   topdir + "/extensions/FixedColumns/js/dataTables.fixedColumns.min.js")
        _copy_file(csspath, zf,
                   topdir + "/extensions/FixedColumns/css/dataTables.fixedColumns.min.css")

    print("Done.")


def _install_bootstrap(jspath, csspath):
    bootstrap_version = "3.3.1"
    bootstrap_url = "https://github.com/twbs/bootstrap/releases/download/"\
        + "v{version}/bootstrap-{version}-dist.zip"\
        .format(version=bootstrap_version)
    sys.stdout.write("Downloading Bootstrap...")
    sys.stdout.flush()
    with NamedTemporaryFile(suffix=".zip", delete=False) as f:
        bootstrap_name = f.name
        f.write(urllib2.urlopen(bootstrap_url).read())

    with ZipFile(bootstrap_name, 'r') as zf:
        _copy_file(jspath, zf, "dist/js/bootstrap.min.js")
        _copy_file(csspath, zf, "dist/css/bootstrap.min.css")
    print("Done.")


def _copy_file(path, zf, fn):
    with zf.open(fn) as f_from:
        with open(op.join(path, op.basename(fn)), 'w') as f_to:
            f_to.write(f_from.read())
