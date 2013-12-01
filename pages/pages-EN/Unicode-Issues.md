## [Unicode Issues](#id31)

HTTP does not directly support Unicode, and neither does this
interface.  All encoding/decoding must be handled by the application;
all strings passed to or from the server must be of type <tt class="docutils literal">str</tt> or
<tt class="docutils literal">bytes</tt>, never <tt class="docutils literal">unicode</tt>.  The result of using a <tt class="docutils literal">unicode</tt>
object where a string object is required, is undefined.

Note also that strings passed to <tt class="docutils literal">start_response()</tt> as a status or
as response headers **must** follow [RFC 2616](http://www.faqs.org/rfcs/rfc2616.html) with respect to encoding.
That is, they must either be ISO-8859-1 characters, or use [RFC 2047](http://www.faqs.org/rfcs/rfc2047.html)
MIME encoding.

On Python platforms where the <tt class="docutils literal">str</tt> or <tt class="docutils literal">StringType</tt> type is in
fact Unicode-based (e.g. Jython, IronPython, Python 3, etc.), all
"strings" referred to in this specification must contain only
code points representable in ISO-8859-1 encoding (<tt class="docutils literal">\u0000</tt> through
<tt class="docutils literal">\u00FF</tt>, inclusive).  It is a fatal error for an application to
supply strings containing any other Unicode character or code point.
Similarly, servers and gateways **must not** supply
strings to an application containing any other Unicode characters.

Again, all objects referred to in this specification as "strings"
**must** be of type <tt class="docutils literal">str</tt> or <tt class="docutils literal">StringType</tt>, and **must not** be
of type <tt class="docutils literal">unicode</tt> or <tt class="docutils literal">UnicodeType</tt>.  And, even if a given platform
allows for more than 8 bits per character in <tt class="docutils literal">str</tt>/<tt class="docutils literal">StringType</tt>
objects, only the lower 8 bits may be used, for any value referred
to in this specification as a "string".

For values referred to in this specification as "bytestrings"
(i.e., values read from <tt class="docutils literal">wsgi.input</tt>, passed to <tt class="docutils literal">write()</tt>
or yielded by the application), the value **must** be of type
<tt class="docutils literal">bytes</tt> under Python 3, and <tt class="docutils literal">str</tt> in earlier versions of
Python.