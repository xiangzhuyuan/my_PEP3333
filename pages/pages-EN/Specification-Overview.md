# [Specification Overview](#id18)

The WSGI interface has two sides: the "server" or "gateway" side, and
the "application" or "framework" side.  The server side invokes a
callable object that is provided by the application side.  The
specifics of how that object is provided are up to the server or
gateway.  It is assumed that some servers or gateways will require an
application's deployer to write a short script to create an instance
of the server or gateway, and supply it with the application object.
Other servers and gateways may use configuration files or other
mechanisms to specify where an application object should be
imported from, or otherwise obtained.

In addition to "pure" servers/gateways and applications/frameworks,
it is also possible to create "middleware" components that implement
both sides of this specification.  Such components act as an
application to their containing server, and as a server to a
contained application, and can be used to provide extended APIs,
content transformation, navigation, and other useful functions.

Throughout this specification, we will use the term "a callable" to
mean "a function, method, class, or an instance with a <tt class="docutils literal">__call__</tt>
method".  It is up to the server, gateway, or application implementing
the callable to choose the appropriate implementation technique for
their needs.  Conversely, a server, gateway, or application that is
invoking a callable **must not** have any dependency on what kind of
callable was provided to it.  Callables are only to be called, not
introspected upon.

## [A Note On String Types](#id19)

In general, HTTP deals with bytes, which means that this specification
is mostly about handling bytes.

However, the content of those bytes often has some kind of textual
interpretation, and in Python, strings are the most convenient way
to handle text.

But in many Python versions and implementations, strings are Unicode,
rather than bytes.  This requires a careful balance between a usable
API and correct translations between bytes and text in the context of
HTTP...  especially to support porting code between Python
implementations with different <tt class="docutils literal">str</tt> types.

WSGI therefore defines two kinds of "string":

*   "Native" strings (which are always implemented using the type
named <tt class="docutils literal">str</tt>) that are used for request/response headers and
metadata
*   "Bytestrings" (which are implemented using the <tt class="docutils literal">bytes</tt> type
in Python 3, and <tt class="docutils literal">str</tt> elsewhere), that are used for the bodies
of requests and responses (e.g. POST/PUT input data and HTML page
outputs).

Do not be confused however: even if Python's <tt class="docutils literal">str</tt> type is actually
Unicode "under the hood", the _content_ of native strings must
still be translatable to bytes via the Latin-1 encoding!  (See
the section on [Unicode Issues](#unicode-issues) later in  this document for more
details.)

In short: where you see the word "string" in this document, it refers
to a "native" string, i.e., an object of type <tt class="docutils literal">str</tt>, whether it is
internally implemented as bytes or unicode.  Where you see references
to "bytestring", this should be read as "an object of type <tt class="docutils literal">bytes</tt>
under Python 3, or type <tt class="docutils literal">str</tt> under Python 2".

And so, even though HTTP is in some sense "really just bytes", there
are  many API conveniences to be had by using whatever Python's
default  <tt class="docutils literal">str</tt> type is.


## [The Application/Framework Side](#id20)

The application object is simply a callable object that accepts
two arguments.  The term "object" should not be misconstrued as
requiring an actual object instance: a function, method, class,
or instance with a <tt class="docutils literal">__call__</tt> method are all acceptable for
use as an application object.  Application objects must be able
to be invoked more than once, as virtually all servers/gateways
(other than CGI) will make such repeated requests.

(Note: although we refer to it as an "application" object, this
should not be construed to mean that application developers will use
WSGI as a web programming API!  It is assumed that application
developers will continue to use existing, high-level framework
services to develop their applications.  WSGI is a tool for
framework and server developers, and is not intended to directly
support application developers.)

Here are two example application objects; one is a function, and the
other is a class:

<pre class="literal-block">HELLO_WORLD = b"Hello world!\n"

def simple_app(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [HELLO_WORLD]

class AppClass:
    """Produce the same output, but using a class

    (Note: 'AppClass' is the "application" here, so calling it
    returns an instance of 'AppClass', which is then the iterable
    return value of the "application callable" as required by
    the spec.

    If we wanted to use *instances* of 'AppClass' as application
    objects instead, we would have to implement a '__call__'
    method, which would be invoked to execute the application,
    and we would need to create an instance for use by the
    server or gateway.
    """

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response

    def __iter__(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield HELLO_WORLD
</pre>

## [The Server/Gateway Side](#id21)

The server or gateway invokes the application callable once for each
request it receives from an HTTP client, that is directed at the
application.  To illustrate, here is a simple CGI gateway, implemented
as a function taking an application object.  Note that this simple
example has limited error handling, because by default an uncaught
exception will be dumped to <tt class="docutils literal">sys.stderr</tt> and logged by the web
server.

<pre class="literal-block">import os, sys

enc, esc = sys.getfilesystemencoding(), 'surrogateescape'

def unicode_to_wsgi(u):
    # Convert an environment variable to a WSGI "bytes-as-unicode" string
    return u.encode(enc, esc).decode('iso-8859-1')

def wsgi_to_bytes(s):
    return s.encode('iso-8859-1')

def run_with_cgi(application):
    environ = {k: unicode_to_wsgi(v) for k,v in os.environ.items()}
    environ['wsgi.input']        = sys.stdin.buffer
    environ['wsgi.errors']       = sys.stderr
    environ['wsgi.version']      = (1, 0)
    environ['wsgi.multithread']  = False
    environ['wsgi.multiprocess'] = True
    environ['wsgi.run_once']     = True

    if environ.get('HTTPS', 'off') in ('on', '1'):
        environ['wsgi.url_scheme'] = 'https'
    else:
        environ['wsgi.url_scheme'] = 'http'

    headers_set = []
    headers_sent = []

    def write(data):
        out = sys.stdout.buffer

        if not headers_set:
             raise AssertionError("write() before start_response()")

        elif not headers_sent:
             # Before the first output, send the stored headers
             status, response_headers = headers_sent[:] = headers_set
             out.write(wsgi_to_bytes('Status: %s\r\n' % status))
             for header in response_headers:
                 out.write(wsgi_to_bytes('%s: %s\r\n' % header))
             out.write(wsgi_to_bytes('\r\n'))

        out.write(data)
        out.flush()

    def start_response(status, response_headers, exc_info=None):
        if exc_info:
            try:
                if headers_sent:
                    # Re-raise original exception if headers sent
                    raise exc_info[1].with_traceback(exc_info[2])
            finally:
                exc_info = None     # avoid dangling circular ref
        elif headers_set:
            raise AssertionError("Headers already set!")

        headers_set[:] = [status, response_headers]

        # Note: error checking on the headers should happen here,
        # *after* the headers are set.  That way, if an error
        # occurs, start_response can only be re-called with
        # exc_info set.

        return write

    result = application(environ, start_response)
    try:
        for data in result:
            if data:    # don't send headers until body appears
                write(data)
        if not headers_sent:
            write('')   # send headers now if body was empty
    finally:
        if hasattr(result, 'close'):
            result.close()
</pre>

## [Middleware: Components that Play Both Sides](#id22)

Note that a single object may play the role of a server with respect
to some application(s), while also acting as an application with
respect to some server(s).  Such "middleware" components can perform
such functions as:

*   Routing a request to different application objects based on the
target URL, after rewriting the <tt class="docutils literal">environ</tt> accordingly.
*   Allowing multiple applications or frameworks to run side-by-side
in the same process
*   Load balancing and remote processing, by forwarding requests and
responses over a network
*   Perform content postprocessing, such as applying XSL stylesheets

The presence of middleware in general is transparent to both the
"server/gateway" and the "application/framework" sides of the
interface, and should require no special support.  A user who
desires to incorporate middleware into an application simply
provides the middleware component to the server, as if it were
an application, and configures the middleware component to
invoke the application, as if the middleware component were a
server.  Of course, the "application" that the middleware wraps
may in fact be another middleware component wrapping another
application, and so on, creating what is referred to as a
"middleware stack".

For the most part, middleware must conform to the restrictions
and requirements of both the server and application sides of
WSGI.  In some cases, however, requirements for middleware
are more stringent than for a "pure" server or application,
and these points will be noted in the specification.

Here is a (tongue-in-cheek) example of a middleware component that
converts <tt class="docutils literal">text/plain</tt> responses to pig latin, using Joe Strout's
<tt class="docutils literal">piglatin.py</tt>.  (Note: a "real" middleware component would
probably use a more robust way of checking the content type, and
should also check for a content encoding.  Also, this simple
example ignores the possibility that a word might be split across
a block boundary.)

<pre class="literal-block">from piglatin import piglatin

class LatinIter:

    """Transform iterated output to piglatin, if it's okay to do so

    Note that the "okayness" can change until the application yields
    its first non-empty bytestring, so 'transform_ok' has to be a mutable
    truth value.
    """

    def __init__(self, result, transform_ok):
        if hasattr(result, 'close'):
            self.close = result.close
        self._next = iter(result).__next__
        self.transform_ok = transform_ok

    def __iter__(self):
        return self

    def __next__(self):
        if self.transform_ok:
            return piglatin(self._next())   # call must be byte-safe on Py3
        else:
            return self._next()

class Latinator:

    # by default, don't transform output
    transform = False

    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):

        transform_ok = []

        def start_latin(status, response_headers, exc_info=None):

            # Reset ok flag, in case this is a repeat call
            del transform_ok[:]

            for name, value in response_headers:
                if name.lower() == 'content-type' and value == 'text/plain':
                    transform_ok.append(True)
                    # Strip content-length if present, else it'll be wrong
                    response_headers = [(name, value)
                        for name, value in response_headers
                            if name.lower() != 'content-length'
                    ]
                    break

            write = start_response(status, response_headers, exc_info)

            if transform_ok:
                def write_latin(data):
                    write(piglatin(data))   # call must be byte-safe on Py3
                return write_latin
            else:
                return write

        return LatinIter(self.application(environ, start_latin), transform_ok)

# Run foo_app under a Latinator's control, using the example CGI gateway
from foo_app import foo_app
run_with_cgi(Latinator(foo_app))
</pre>

