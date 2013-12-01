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

