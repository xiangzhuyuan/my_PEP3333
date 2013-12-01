# [Implementation/Application Notes](#id36)

## [Server Extension APIs](#id37)

Some server authors may wish to expose more advanced APIs, that
application or framework authors can use for specialized purposes.
For example, a gateway based on <tt class="docutils literal">mod_python</tt> might wish to expose
part of the Apache API as a WSGI extension.

In the simplest case, this requires nothing more than defining an
<tt class="docutils literal">environ</tt> variable, such as <tt class="docutils literal">mod_python.some_api</tt>.  But, in many
cases, the possible presence of middleware can make this difficult.
For example, an API that offers access to the same HTTP headers that
are found in <tt class="docutils literal">environ</tt> variables, might return different data if
<tt class="docutils literal">environ</tt> has been modified by middleware.

In general, any extension API that duplicates, supplants, or bypasses
some portion of WSGI functionality runs the risk of being incompatible
with middleware components.  Server/gateway developers should _not_
assume that nobody will use middleware, because some framework
developers specifically intend to organize or reorganize their
frameworks to function almost entirely as middleware of various kinds.

So, to provide maximum compatibility, servers and gateways that
provide extension APIs that replace some WSGI functionality, **must**
design those APIs so that they are invoked using the portion of the
API that they replace.  For example, an extension API to access HTTP
request headers must require the application to pass in its current
<tt class="docutils literal">environ</tt>, so that the server/gateway may verify that HTTP headers
accessible via the API have not been altered by middleware.  If the
extension API cannot guarantee that it will always agree with
<tt class="docutils literal">environ</tt> about the contents of HTTP headers, it must refuse service
to the application, e.g. by raising an error, returning <tt class="docutils literal">None</tt>
instead of a header collection, or whatever is appropriate to the API.

Similarly, if an extension API provides an alternate means of writing
response data or headers, it should require the <tt class="docutils literal">start_response</tt>
callable to be passed in, before the application can obtain the
extended service.  If the object passed in is not the same one that
the server/gateway originally supplied to the application, it cannot
guarantee correct operation and must refuse to provide the extended
service to the application.

These guidelines also apply to middleware that adds information such
as parsed cookies, form variables, sessions, and the like to
<tt class="docutils literal">environ</tt>.  Specifically, such middleware should provide these
features as functions which operate on <tt class="docutils literal">environ</tt>, rather than simply
stuffing values into <tt class="docutils literal">environ</tt>.  This helps ensure that information
is calculated from <tt class="docutils literal">environ</tt> _after_ any middleware has done any URL
rewrites or other <tt class="docutils literal">environ</tt> modifications.

It is very important that these "safe extension" rules be followed by
both server/gateway and middleware developers, in order to avoid a
future in which middleware developers are forced to delete any and all
extension APIs from <tt class="docutils literal">environ</tt> to ensure that their mediation isn't
being bypassed by applications using those extensions!


## [Application Configuration](#id38)

This specification does not define how a server selects or obtains an
application to invoke.  These and other configuration options are
highly server-specific matters.  It is expected that server/gateway
authors will document how to configure the server to execute a
particular application object, and with what options (such as
threading options).

Framework authors, on the other hand, should document how to create an
application object that wraps their framework's functionality.  The
user, who has chosen both the server and the application framework,
must connect the two together.  However, since both the framework and
the server now have a common interface, this should be merely a
mechanical matter, rather than a significant engineering effort for
each new server/framework pair.

Finally, some applications, frameworks, and middleware may wish to
use the <tt class="docutils literal">environ</tt> dictionary to receive simple string configuration
options.  Servers and gateways **should** support this by allowing
an application's deployer to specify name-value pairs to be placed in
<tt class="docutils literal">environ</tt>.  In the simplest case, this support can consist merely of
copying all operating system-supplied environment variables from
<tt class="docutils literal">os.environ</tt> into the <tt class="docutils literal">environ</tt> dictionary, since the deployer in
principle can configure these externally to the server, or in the
CGI case they may be able to be set via the server's configuration
files.

Applications **should** try to keep such required variables to a
minimum, since not all servers will support easy configuration of
them.  Of course, even in the worst case, persons deploying an
application can create a script to supply the necessary configuration
values:

<pre class="literal-block">from the_app import application

def new_app(environ, start_response):
    environ['the_app.configval1'] = 'something'
    return application(environ, start_response)
</pre>

But, most existing applications and frameworks will probably only need
a single configuration value from <tt class="docutils literal">environ</tt>, to indicate the location
of their application or framework-specific configuration file(s).  (Of
course, applications should cache such configuration, to avoid having
to re-read it upon each invocation.)



## [URL Reconstruction](#id39)

If an application wishes to reconstruct a request's complete URL, it
may do so using the following algorithm, contributed by Ian Bicking:

<pre class="literal-block">from urllib import quote
url = environ['wsgi.url_scheme']+'://'

if environ.get('HTTP_HOST'):
    url += environ['HTTP_HOST']
else:
    url += environ['SERVER_NAME']

    if environ['wsgi.url_scheme'] == 'https':
        if environ['SERVER_PORT'] != '443':
           url += ':' + environ['SERVER_PORT']
    else:
        if environ['SERVER_PORT'] != '80':
           url += ':' + environ['SERVER_PORT']

url += quote(environ.get('SCRIPT_NAME', ''))
url += quote(environ.get('PATH_INFO', ''))
if environ.get('QUERY_STRING'):
    url += '?' + environ['QUERY_STRING']
</pre>

Note that such a reconstructed URL may not be precisely the same URI
as requested by the client.  Server rewrite rules, for example, may
have modified the client's originally requested URL to place it in a
canonical form.



## [Supporting Older (&lt;2.2) Versions of Python](#id40)

Some servers, gateways, or applications may wish to support older
(&lt;2.2) versions of Python.  This is especially important if Jython
is a target platform, since as of this writing a production-ready
version of Jython 2.2 is not yet available.

For servers and gateways, this is relatively straightforward:
servers and gateways targeting pre-2.2 versions of Python must
simply restrict themselves to using only a standard "for" loop to
iterate over any iterable returned by an application.  This is the
only way to ensure source-level compatibility with both the pre-2.2
iterator protocol (discussed further below) and "today's" iterator
protocol (see [PEP 234](/dev/peps/pep-0234)).

(Note that this technique necessarily applies only to servers,
gateways, or middleware that are written in Python.  Discussion of
how to use iterator protocol(s) correctly from other languages is
outside the scope of this PEP.)

For applications, supporting pre-2.2 versions of Python is slightly
more complex:

*   You may not return a file object and expect it to work as an iterable,
since before Python 2.2, files were not iterable.  (In general, you
shouldn't do this anyway, because it will perform quite poorly most
of the time!)  Use <tt class="docutils literal">wsgi.file_wrapper</tt> or an application-specific
file wrapper class.  (See [Optional Platform-Specific File Handling](#optional-platform-specific-file-handling)
for more on <tt class="docutils literal">wsgi.file_wrapper</tt>, and an example class you can use
to wrap a file as an iterable.)
*   If you return a custom iterable, it **must** implement the pre-2.2
iterator protocol.  That is, provide a <tt class="docutils literal">__getitem__</tt> method that
accepts an integer key, and raises <tt class="docutils literal">IndexError</tt> when exhausted.
(Note that built-in sequence types are also acceptable, since they
also implement this protocol.)

Finally, middleware that wishes to support pre-2.2 versions of Python,
and iterates over application return values or itself returns an
iterable (or both), must follow the appropriate recommendations above.

(Note: It should go without saying that to support pre-2.2 versions
of Python, any server, gateway, application, or middleware must also
use only language features available in the target version, use
1 and 0 instead of <tt class="docutils literal">True</tt> and <tt class="docutils literal">False</tt>, etc.)



## [Optional Platform-Specific File Handling](#id41)

Some operating environments provide special high-performance file-
transmission facilities, such as the Unix <tt class="docutils literal">sendfile()</tt> call.
Servers and gateways **may** expose this functionality via an optional
<tt class="docutils literal">wsgi.file_wrapper</tt> key in the <tt class="docutils literal">environ</tt>.  An application
**may** use this "file wrapper" to convert a file or file-like object
into an iterable that it then returns, e.g.:

<pre class="literal-block">if 'wsgi.file_wrapper' in environ:
    return environ['wsgi.file_wrapper'](filelike, block_size)
else:
    return iter(lambda: filelike.read(block_size), '')
</pre>

If the server or gateway supplies <tt class="docutils literal">wsgi.file_wrapper</tt>, it must be
a callable that accepts one required positional parameter, and one
optional positional parameter.  The first parameter is the file-like
object to be sent, and the second parameter is an optional block
size "suggestion" (which the server/gateway need not use).  The
callable **must** return an iterable object, and **must not** perform
any data transmission until and unless the server/gateway actually
receives the iterable as a return value from the application.
(To do otherwise would prevent middleware from being able to interpret
or override the response data.)

To be considered "file-like", the object supplied by the application
must have a <tt class="docutils literal">read()</tt> method that takes an optional size argument.
It **may** have a <tt class="docutils literal">close()</tt> method, and if so, the iterable returned
by <tt class="docutils literal">wsgi.file_wrapper</tt> **must** have a <tt class="docutils literal">close()</tt> method that
invokes the original file-like object's <tt class="docutils literal">close()</tt> method.  If the
"file-like" object has any other methods or attributes with names
matching those of Python built-in file objects (e.g. <tt class="docutils literal">fileno()</tt>),
the <tt class="docutils literal">wsgi.file_wrapper</tt> **may** assume that these methods or
attributes have the same semantics as those of a built-in file object.

The actual implementation of any platform-specific file handling
must occur **after** the application returns, and the server or
gateway checks to see if a wrapper object was returned.  (Again,
because of the presence of middleware, error handlers, and the like,
it is not guaranteed that any wrapper created will actually be used.)

Apart from the handling of <tt class="docutils literal">close()</tt>, the semantics of returning a
file wrapper from the application should be the same as if the
application had returned <tt class="docutils literal">iter(filelike.read, '')</tt>.  In other words,
transmission should begin at the current position within the "file"
at the time that transmission begins, and continue until the end is
reached, or until <tt class="docutils literal"><span class="pre">Content-Length</span></tt> bytes have been written.  (If
the application doesn't supply a <tt class="docutils literal"><span class="pre">Content-Length</span></tt>, the server **may**
generate one from the file using its knowledge of the underlying file
implementation.)

Of course, platform-specific file transmission APIs don't usually
accept arbitrary "file-like" objects.  Therefore, a
<tt class="docutils literal">wsgi.file_wrapper</tt> has to introspect the supplied object for
things such as a <tt class="docutils literal">fileno()</tt> (Unix-like OSes) or a
<tt class="docutils literal">java.nio.FileChannel</tt> (under Jython) in order to determine if
the file-like object is suitable for use with the platform-specific
API it supports.

Note that even if the object is _not_ suitable for the platform API,
the <tt class="docutils literal">wsgi.file_wrapper</tt> **must** still return an iterable that wraps
<tt class="docutils literal">read()</tt> and <tt class="docutils literal">close()</tt>, so that applications using file wrappers
are portable across platforms.  Here's a simple platform-agnostic
file wrapper class, suitable for old (pre 2.2) and new Pythons alike:

<pre class="literal-block">class FileWrapper:

    def __init__(self, filelike, blksize=8192):
        self.filelike = filelike
        self.blksize = blksize
        if hasattr(filelike, 'close'):
            self.close = filelike.close

    def __getitem__(self, key):
        data = self.filelike.read(self.blksize)
        if data:
            return data
        raise IndexError
</pre>

and here is a snippet from a server/gateway that uses it to provide
access to a platform-specific API:

<pre class="literal-block">environ['wsgi.file_wrapper'] = FileWrapper
result = application(environ, start_response)

try:
    if isinstance(result, FileWrapper):
        # check if result.filelike is usable w/platform-specific
        # API, and if so, use that API to transmit the result.
        # If not, fall through to normal iterable handling
        # loop below.

    for data in result:
        # etc.

finally:
    if hasattr(result, 'close'):
        result.close()
</pre>

