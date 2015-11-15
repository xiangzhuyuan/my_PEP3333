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

