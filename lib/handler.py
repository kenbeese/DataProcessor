# coding:utf-8

import cgi
import os
import time


_weekdayname = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
_monthname = [None, "Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


class Request(object):

    """A class handling HTTP requests."""

    def __init__(self, environ={}):
        self.form = cgi.FieldStorage()
        self.environ = environ

    def get(self, name):
        """ get value of request

        Parameters
        ----------
        name: str
            key of the request

        Returns
        -------
        str
            the value of request

        Raises
        ------
        KeyError
            raises if request does not have element with `name`

        """
        return self.form[name].value

    def has(self, name):
        """ ask whether request has `name`

        Parameters
        ----------
        name: str
            key of the request

        Returns
        -------
        bool

        """
        return (name in req.form)


class Response(object):

    """The class handring Response of HTTP.

    You can use this class by making instance of this class
    before sending Response.

    Examples
    --------
    * JSON
    >>> res = Response("json")
    >>> res.set_body("{'exit_code' : 0}")
    >>> print(res) # doctest: +SKIP

    * HTML
    >>> res = Response("html")
    >>> res.set_body('''
    ...     <!DOCTYPE html>
    ...     <html>
    ...         <body>
    ...             <h1>My Home Page!</h1>
    ...         </body>
    ...     </html>
    ...     ''')
    >>> print(res) # doctest: +SKIP

    """

    def __init__(self, content_type="html", charset='utf-8'):
        if content_type == "html":
            self.headers = {'Content-type': 'text/html;charset=%s' % charset}
        elif content_type == "json":
            self.headers = {'Content-type': 'application/json; charset=%s'
                                            % charset}
        elif content_type == "xml":
            self.headers = {'Content-type': 'text/xml; charset=%s' % charset}
        else:
            raise RuntimeError("content_type must be in {html, json, xml}")
        self.status = 200
        self.status_message = 'success'
        self.body = ""

    def set_header(self,  name,  value):
        """Set header of Response."""
        self.headers[name] = value

    def get_header(self, name):
        """Get the header which already set and return object."""
        return self.headers.get(name, None)

    def set_body(self, bodystr):
        """Set the body of response.

        See Examples of this class.

        """
        self.body = bodystr

    def make_output(self, timestamp=None):
        """Make Response text including header and text and return str."""
        if timestamp is None:
            timestamp = time.time()
        year, month, day, hh, mm, ss, wd, y, z = time.gmtime(timestamp)
        dtstr = ("%s, %02d %3s %4d %02d:%02d:%02d GMT"
                 % (_weekdayname[wd], day, _monthname[month],
                    year, hh, mm, ss))
        self.set_header("Last-Modified", dtstr)
        headers = '\n'.join(["%s: %s" % (key, self.headers[key])
                             for key in self.headers])
        return headers+'\n\n'+self.body

    def __str__(self):
        """Convert Request and return string."""
        return self.make_output()


def operation_success():
    res = Response("json")
    res.set_body(u"""
    {"exit_code" : 0}
    """)
    print(res)


def operation_fail(msg="", code=1):
    res = Response("json")
    res.status = 500
    res.status_message = "internal server error"
    res.set_body("""
    {"exit_code" : %d, "message" : "%s" }
    """ % (code, msg))
    print(res)
