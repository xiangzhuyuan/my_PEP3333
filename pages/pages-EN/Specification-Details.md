# [Specification Details](#id23)

The application object must accept two positional arguments.  For
the sake of illustration, we have named them <tt class="docutils literal">environ</tt> and
<tt class="docutils literal">start_response</tt>, but they are not required to have these names.
A server or gateway **must** invoke the application object using
positional (not keyword) arguments.  (E.g. by calling
<tt class="docutils literal">result = application(environ, start_response)</tt> as shown above.)

The <tt class="docutils literal">environ</tt> parameter is a dictionary object, containing CGI-style
environment variables.  This object **must** be a builtin Python
dictionary (_not_ a subclass, <tt class="docutils literal">UserDict</tt> or other dictionary
emulation), and the application is allowed to modify the dictionary
in any way it desires.  The dictionary must also include certain
WSGI-required variables (described in a later section), and may
also include server-specific extension variables, named according
to a convention that will be described below.

The <tt class="docutils literal">start_response</tt> parameter is a callable accepting two
required positional arguments, and one optional argument.  For the sake
of illustration, we have named these arguments <tt class="docutils literal">status</tt>,
<tt class="docutils literal">response_headers</tt>, and <tt class="docutils literal">exc_info</tt>, but they are not required to
have these names, and the application **must** invoke the
<tt class="docutils literal">start_response</tt> callable using positional arguments (e.g.
<tt class="docutils literal">start_response(status, response_headers)</tt>).

The <tt class="docutils literal">status</tt> parameter is a status string of the form
<tt class="docutils literal">"999 Message here"</tt>, and <tt class="docutils literal">response_headers</tt> is a list of
<tt class="docutils literal">(header_name, header_value)</tt> tuples describing the HTTP response
header.  The optional <tt class="docutils literal">exc_info</tt> parameter is described below in the
sections on [The start_response() Callable](#the-start-response-callable) and [Error Handling](#error-handling).
It is used only when the application has trapped an error and is
attempting to display an error message to the browser.

The <tt class="docutils literal">start_response</tt> callable must return a <tt class="docutils literal">write(body_data)</tt>
callable that takes one positional parameter: a bytestring to be written
as part of the HTTP response body.  (Note: the <tt class="docutils literal">write()</tt> callable is
provided only to support certain existing frameworks' imperative output
APIs; it should not be used by new applications or frameworks if it
can be avoided.  See the [Buffering and Streaming](#buffering-and-streaming) section for more
details.)

When called by the server, the application object must return an
iterable yielding zero or more bytestrings.  This can be accomplished in a
variety of ways, such as by returning a list of bytestrings, or by the
application being a generator function that yields bytestrings, or
by the application being a class whose instances are iterable.
Regardless of how it is accomplished, the application object must
always return an iterable yielding zero or more bytestrings.

The server or gateway must transmit the yielded bytestrings to the client
in an unbuffered fashion, completing the transmission of each bytestring
before requesting another one.  (In other words, applications
**should** perform their own buffering.  See the [Buffering and
Streaming](#buffering-and-streaming) section below for more on how application output must be
handled.)

The server or gateway should treat the yielded bytestrings as binary byte
sequences: in particular, it should ensure that line endings are
not altered.  The application is responsible for ensuring that the
bytestring(s) to be written are in a format suitable for the client.  (The
server or gateway **may** apply HTTP transfer encodings, or perform
other transformations for the purpose of implementing HTTP features
such as byte-range transmission.  See [Other HTTP Features](#other-http-features), below,
for more details.)

If a call to <tt class="docutils literal">len(iterable)</tt> succeeds, the server must be able
to rely on the result being accurate.  That is, if the iterable
returned by the application provides a working <tt class="docutils literal">__len__()</tt>
method, it **must** return an accurate result.  (See
the [Handling the Content-Length Header](#handling-the-content-length-header) section for information
on how this would normally be used.)

If the iterable returned by the application has a <tt class="docutils literal">close()</tt> method,
the server or gateway **must** call that method upon completion of the
current request, whether the request was completed normally, or
terminated early due to an application error during iteration or an early
disconnect of the browser.  (The <tt class="docutils literal">close()</tt> method requirement is to
support resource release by the application.  This protocol is intended
to complement [PEP 342](/dev/peps/pep-0342)'s generator support, and other common iterables
with <tt class="docutils literal">close()</tt> methods.)

Applications returning a generator or other custom iterator **should not**
assume the entire iterator will be consumed, as it **may** be closed early
by the server.

(Note: the application **must** invoke the <tt class="docutils literal">start_response()</tt>
callable before the iterable yields its first body bytestring, so that the
server can send the headers before any body content.  However, this
invocation **may** be performed by the iterable's first iteration, so
servers **must not** assume that <tt class="docutils literal">start_response()</tt> has been called
before they begin iterating over the iterable.)

Finally, servers and gateways **must not** directly use any other
attributes of the iterable returned by the application, unless it is an
instance of a type specific to that server or gateway, such as a "file
wrapper" returned by <tt class="docutils literal">wsgi.file_wrapper</tt> (see [Optional
Platform-Specific File Handling](#optional-platform-specific-file-handling)).  In the general case, only
attributes specified here, or accessed via e.g. the [PEP 234](/dev/peps/pep-0234) iteration
APIs are acceptable.
