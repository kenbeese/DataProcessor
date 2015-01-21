# -*- coding: utf-8 -*-

import os
import sys
import os.path as op
import urllib2
from zipfile import ZipFile
from tempfile import NamedTemporaryFile
from daemon import DaemonContext
from daemon.pidfile import PIDLockFile
from functools import wraps


sys.path = ([sys.path[0]]
            + [os.path.join(os.path.dirname(__file__), "../lib")]
            + sys.path[1:])
from dataprocessor import utility, exception, rc
sys.path = [sys.path[0]] + sys.path[2:]


from webapp import app

ROOT = op.dirname(__file__)


def argparser():
    parser = rc.ArgumentParser()
    sub_psr = parser.add_subparsers()

    port_cfg = {
        "default": 8080,
        "help": "Port for the server"
    }
    logfilepath_cfg = {
        "default": os.path.join(ROOT, "server.log"),
        "help": "The name of the log file",
    }
    lockfile_cfg = {
        "default": "/tmp/DataProcessorServer.pid",
        "help": "Lock filename",
    }

    # start
    start_psr = sub_psr.add_parser("start",
                                   help="start DataProcessor server daemon")
    start_psr.set_defaults(func=start)
    rc.load_into_argparse(start_psr, "dpserver", {
        "port": port_cfg,
        "logfilepath": logfilepath_cfg,
        "lockfile": lockfile_cfg,
    }, allow_empty=True)

    # debug
    debug_psr = sub_psr.add_parser("debug",
                                   help="start DataProcessor server with debug-mode")
    debug_psr.set_defaults(func=debug)
    rc.load_into_argparse(debug_psr, "dpserver", {
        "port": port_cfg,
    }, allow_empty=True)

    # stop
    stop_psr = sub_psr.add_parser("stop", help="kill articles server")
    stop_psr.set_defaults(func=stop)
    rc.load_into_argparse(stop_psr, "dpserver", {
        "lockfile": lockfile_cfg,
    }, allow_empty=True)

    # install
    install_psr = sub_psr.add_parser("install", help="install jQuery")
    install_psr.set_defaults(func=install)
    return parser


def start(args):
    port = int(args.port)
    log_path = args.logfilepath
    lock_path = args.lockfile
    data_path = utility.check_file(args.json)
    app.config["DATA_PATH"] = data_path
    if not op.exists(lock_path):
        dc = DaemonContext(pidfile=PIDLockFile(lock_path),
                           stderr=open(log_path, "w+"),
                           working_directory=ROOT)
        with dc:
            app.run(port=port)
    else:
        raise exception.DataProcessorError("Server already stands.")


def debug(args):
    port = int(args.port)
    data_path = utility.check_file(args.json)
    app.config["DATA_PATH"] = data_path
    app.run(debug=True, port=port)


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
    jspath = op.join(ROOT, "static/js")
    csspath = op.join(ROOT, "static/css")
    imagepath = op.join(ROOT, "static/images")
    fontspath = op.join(ROOT, "static/fonts")
    if not os.path.exists(imagepath):
        os.mkdir(imagepath)
    if not os.path.exists(fontspath):
        os.mkdir(fontspath)

    _install_jquery(jspath)
    _install_jquery_cookie(jspath)
    _install_jquery_blockUI(jspath)
    _install_jquery_datatables(jspath, csspath, imagepath)
    _install_bootstrap(jspath, csspath, fontspath)


def show_progress(name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwds):
            sys.stdout.write("Downloading {}...".format(name))
            sys.stdout.flush()
            res = f(*args, **kwds)
            print("Done")
            return res
        return wrapper
    return decorator


@show_progress("jQuery")
def _install_jquery(jspath):
    jquery_filename = "jquery-1.10.2.js"
    jquery_url = "http://code.jquery.com/" + jquery_filename
    with open(op.join(jspath, jquery_filename), "w") as f:
        f.write(urllib2.urlopen(jquery_url).read())


@show_progress("jQuery Cookie")
def _install_jquery_cookie(jspath):
    jquery_cookie_filename = "jquery.cookie.js"
    jquery_cookie_url = "https://raw.github.com/carhartl/jquery-cookie/master/src/"\
        + jquery_cookie_filename
    with open(op.join(jspath, jquery_cookie_filename), "w") as f:
        f.write(urllib2.urlopen(jquery_cookie_url).read())


@show_progress("jQuery blockUI")
def _install_jquery_blockUI(jspath):
    jquery_blockUI_filename = "jquery.blockUI.js"
    jquery_blockUI_url = "http://malsup.github.io/" + jquery_blockUI_filename
    with open(op.join(jspath, jquery_blockUI_filename), "w") as f:
        f.write(urllib2.urlopen(jquery_blockUI_url).read())


@show_progress("jQuery datatables")
def _install_jquery_datatables(jspath, csspath, imagepath):
    version = "1.10.4"
    topdir = "DataTables-{}".format(version)
    url = "http://datatables.net/releases/{}.zip".format(topdir)

    req = urllib2.Request(url,
                          headers={'User-Agent': "Magic Browser"})
    with NamedTemporaryFile(suffix=".zip", delete=False) as f:
        zipname = f.name
        f.write(urllib2.urlopen(req).read())

    with ZipFile(zipname, 'r') as zf:
        _copy_file(jspath, zf,
                   topdir + "/media/js/jquery.dataTables.min.js")
        _copy_file(csspath, zf,
                   topdir + "/media/css/jquery.dataTables.min.css")
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


@show_progress("Bootstrap")
def _install_bootstrap(jspath, csspath, fontspath):
    bootstrap_version = "3.3.1"
    bootstrap_url = "https://github.com/twbs/bootstrap/releases/download/"\
        + "v{version}/bootstrap-{version}-dist.zip"\
        .format(version=bootstrap_version)
    with NamedTemporaryFile(suffix=".zip", delete=False) as f:
        bootstrap_name = f.name
        f.write(urllib2.urlopen(bootstrap_url).read())

    with ZipFile(bootstrap_name, 'r') as zf:
        _copy_file(jspath, zf, "dist/js/bootstrap.min.js")
        _copy_file(csspath, zf, "dist/css/bootstrap.min.css")
        _copy_file(fontspath, zf, "dist/fonts/glyphicons-halflings-regular.eot")
        _copy_file(fontspath, zf, "dist/fonts/glyphicons-halflings-regular.svg")
        _copy_file(fontspath, zf, "dist/fonts/glyphicons-halflings-regular.ttf")
        _copy_file(fontspath, zf, "dist/fonts/glyphicons-halflings-regular.woff")


def _copy_file(path, zf, fn):
    with zf.open(fn) as f_from:
        with open(op.join(path, op.basename(fn)), 'w') as f_to:
            f_to.write(f_from.read())
