
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

