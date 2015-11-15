## [The <tt class="docutils literal">start_response()</tt> Callable](#id26)

The second parameter passed to the application object is a callable
of the form <tt class="docutils literal">start_response(status, response_headers, exc_info=None)</tt>.
(As with all WSGI callables, the arguments must be supplied
positionally, not by keyword.)  The <tt class="docutils literal">start_response</tt> callable is
used to begin the HTTP response, and it must return a
<tt class="docutils literal">write(body_data)</tt> callable (see the [Buffering and Streaming](#buffering-and-streaming)
section, below).

The <tt class="docutils literal">status</tt> argument is an HTTP "status" string like <tt class="docutils literal">"200 OK"</tt>
or <tt class="docutils literal">"404 Not Found"</tt>.  That is, it is a string consisting of a
Status-Code and a Reason-Phrase, in that order and separated by a
single space, with no surrounding whitespace or other characters.
(See [RFC 2616](http://www.faqs.org/rfcs/rfc2616.html), Section 6.1.1 for more information.)  The string
**must not** contain control characters, and must not be terminated
with a carriage return, linefeed, or combination thereof.

The <tt class="docutils literal">response_headers</tt> argument is a list of <tt class="docutils literal">(header_name,
header_value)</tt> tuples.  It must be a Python list; i.e.
<tt class="docutils literal">type(response_headers) is ListType</tt>, and the server **may** change
its contents in any way it desires.  Each <tt class="docutils literal">header_name</tt> must be a
valid HTTP header field-name (as defined by [RFC 2616](http://www.faqs.org/rfcs/rfc2616.html), Section 4.2),
without a trailing colon or other punctuation.

Each <tt class="docutils literal">header_value</tt> **must not** include _any_ control characters,
including carriage returns or linefeeds, either embedded or at the end.
(These requirements are to minimize the complexity of any parsing that
must be performed by servers, gateways, and intermediate response
processors that need to inspect or modify response headers.)

In general, the server or gateway is responsible for ensuring that
correct headers are sent to the client: if the application omits
a header required by HTTP (or other relevant specifications that are in
effect), the server or gateway **must** add it.  For example, the HTTP
<tt class="docutils literal">Date:</tt> and <tt class="docutils literal">Server:</tt> headers would normally be supplied by the
server or gateway.

(A reminder for server/gateway authors: HTTP header names are
case-insensitive, so be sure to take that into consideration when
examining application-supplied headers!)

Applications and middleware are forbidden from using HTTP/1.1
"hop-by-hop" features or headers, any equivalent features in HTTP/1.0,
or any headers that would affect the persistence of the client's
connection to the web server.  These features are the
exclusive province of the actual web server, and a server or gateway
**should** consider it a fatal error for an application to attempt
sending them, and raise an error if they are supplied to
<tt class="docutils literal">start_response()</tt>.  (For more specifics on "hop-by-hop" features and
headers, please see the [Other HTTP Features](#other-http-features) section below.)

Servers **should** check for errors in the headers at the time
<tt class="docutils literal">start_response</tt> is called, so that an error can be raised while
the application is still running.

However, the <tt class="docutils literal">start_response</tt> callable **must not** actually transmit the
response headers.  Instead, it must store them for the server or
gateway to transmit **only** after the first iteration of the
application return value that yields a non-empty bytestring, or upon
the application's first invocation of the <tt class="docutils literal">write()</tt> callable.  In
other words, response headers must not be sent until there is actual
body data available, or until the application's returned iterable is
exhausted.  (The only possible exception to this rule is if the
response headers explicitly include a <tt class="docutils literal"><span class="pre">Content-Length</span></tt> of zero.)

This delaying of response header transmission is to ensure that buffered
and asynchronous applications can replace their originally intended
output with error output, up until the last possible moment.  For
example, the application may need to change the response status from
"200 OK" to "500 Internal Error", if an error occurs while the body is
being generated within an application buffer.

The <tt class="docutils literal">exc_info</tt> argument, if supplied, must be a Python
<tt class="docutils literal">sys.exc_info()</tt> tuple.  This argument should be supplied by the
application only if <tt class="docutils literal">start_response</tt> is being called by an error
handler.  If <tt class="docutils literal">exc_info</tt> is supplied, and no HTTP headers have been
output yet, <tt class="docutils literal">start_response</tt> should replace the currently-stored
HTTP response headers with the newly-supplied ones, thus allowing the
application to "change its mind" about the output when an error has
occurred.

However, if <tt class="docutils literal">exc_info</tt> is provided, and the HTTP headers have already
been sent, <tt class="docutils literal">start_response</tt> **must** raise an error, and **should**
re-raise using the <tt class="docutils literal">exc_info</tt> tuple.  That is:

<pre class="literal-block">raise exc_info[1].with_traceback(exc_info[2])
</pre>

This will re-raise the exception trapped by the application, and in
principle should abort the application.  (It is not safe for the
application to attempt error output to the browser once the HTTP
headers have already been sent.)  The application **must not** trap
any exceptions raised by <tt class="docutils literal">start_response</tt>, if it called
<tt class="docutils literal">start_response</tt> with <tt class="docutils literal">exc_info</tt>.  Instead, it should allow
such exceptions to propagate back to the server or gateway.  See
[Error Handling](#error-handling) below, for more details.

The application **may** call <tt class="docutils literal">start_response</tt> more than once, if and
only if the <tt class="docutils literal">exc_info</tt> argument is provided.  More precisely, it is
a fatal error to call <tt class="docutils literal">start_response</tt> without the <tt class="docutils literal">exc_info</tt>
argument if <tt class="docutils literal">start_response</tt> has already been called within the
current invocation of the application.  This includes the case where
the first call to <tt class="docutils literal">start_response</tt> raised an error.  (See the example
CGI gateway above for an illustration of the correct logic.)

Note: servers, gateways, or middleware implementing <tt class="docutils literal">start_response</tt>
**should** ensure that no reference is held to the <tt class="docutils literal">exc_info</tt>
parameter beyond the duration of the function's execution, to avoid
creating a circular reference through the traceback and frames
involved.  The simplest way to do this is something like:

<pre class="literal-block">def start_response(status, response_headers, exc_info=None):
    if exc_info:
         try:
             # do stuff w/exc_info here
         finally:
             exc_info = None    # Avoid circular ref.
</pre>

The example CGI gateway provides another illustration of this
technique.
