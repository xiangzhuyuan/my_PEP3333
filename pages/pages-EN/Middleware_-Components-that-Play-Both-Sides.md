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