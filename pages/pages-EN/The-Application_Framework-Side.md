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