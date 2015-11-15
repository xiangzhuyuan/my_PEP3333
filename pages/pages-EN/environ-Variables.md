## [<tt class="docutils literal">environ</tt> Variables](#id24)

The <tt class="docutils literal">environ</tt> dictionary is required to contain these CGI
environment variables, as defined by the Common Gateway Interface
specification [[2]](#id9).  The following variables **must** be present,
unless their value would be an empty string, in which case they
**may** be omitted, except as otherwise noted below.

<dl class="docutils">
<dt><tt class="docutils literal">REQUEST_METHOD</tt></dt>
<dd>The HTTP request method, such as <tt class="docutils literal">"GET"</tt> or <tt class="docutils literal">"POST"</tt>.  This
cannot ever be an empty string, and so is always required.</dd>
<dt><tt class="docutils literal">SCRIPT_NAME</tt></dt>
<dd>The initial portion of the request URL's "path" that corresponds to
the application object, so that the application knows its virtual
"location".  This **may** be an empty string, if the application
corresponds to the "root" of the server.</dd>
<dt><tt class="docutils literal">PATH_INFO</tt></dt>
<dd>The remainder of the request URL's "path", designating the virtual
"location" of the request's target within the application.  This
**may** be an empty string, if the request URL targets the
application root and does not have a trailing slash.</dd>
<dt><tt class="docutils literal">QUERY_STRING</tt></dt>
<dd>The portion of the request URL that follows the <tt class="docutils literal"><span class="pre">"?"</span></tt>, if any.
May be empty or absent.</dd>
<dt><tt class="docutils literal">CONTENT_TYPE</tt></dt>
<dd>The contents of any <tt class="docutils literal"><span class="pre">Content-Type</span></tt> fields in the HTTP request.
May be empty or absent.</dd>
<dt><tt class="docutils literal">CONTENT_LENGTH</tt></dt>
<dd>The contents of any <tt class="docutils literal"><span class="pre">Content-Length</span></tt> fields in the HTTP request.
May be empty or absent.</dd>
<dt><tt class="docutils literal">SERVER_NAME</tt>, <tt class="docutils literal">SERVER_PORT</tt></dt>
<dd>When combined with <tt class="docutils literal">SCRIPT_NAME</tt> and <tt class="docutils literal">PATH_INFO</tt>, these two strings
can be used to complete the URL.  Note, however, that <tt class="docutils literal">HTTP_HOST</tt>,
if present, should be used in   preference to <tt class="docutils literal">SERVER_NAME</tt> for
reconstructing the request URL.  See the [URL Reconstruction](#url-reconstruction)
section below for more detail.   <tt class="docutils literal">SERVER_NAME</tt> and <tt class="docutils literal">SERVER_PORT</tt>
can never be empty strings, and so are always required.</dd>
<dt><tt class="docutils literal">SERVER_PROTOCOL</tt></dt>
<dd>The version of the protocol the client used to send the request.
Typically this will be something like <tt class="docutils literal">"HTTP/1.0"</tt> or <tt class="docutils literal">"HTTP/1.1"</tt>
and may be used by the application to determine how to treat any
HTTP request headers.  (This variable should probably be called
<tt class="docutils literal">REQUEST_PROTOCOL</tt>, since it denotes the protocol used in the
request, and is not necessarily the protocol that will be used in the
server's response.  However, for compatibility with CGI we have to
keep the existing name.)</dd>
<dt><tt class="docutils literal">HTTP_</tt> Variables</dt>
<dd>Variables corresponding to the client-supplied HTTP request headers
(i.e., variables whose names begin with <tt class="docutils literal">"HTTP_"</tt>).  The presence or
absence of these variables should correspond with the presence or
absence of the appropriate HTTP header in the request.</dd>
</dl>

A server or gateway **should** attempt to provide as many other CGI
variables as are applicable.  In addition, if SSL is in use, the server
or gateway **should** also provide as many of the Apache SSL environment
variables [[5]](#id12) as are applicable, such as <tt class="docutils literal">HTTPS=on</tt> and
<tt class="docutils literal">SSL_PROTOCOL</tt>.  Note, however, that an application that uses any CGI
variables other than the ones listed above are necessarily non-portable
to web servers that do not support the relevant extensions.  (For
example, web servers that do not publish files will not be able to
provide a meaningful <tt class="docutils literal">DOCUMENT_ROOT</tt> or <tt class="docutils literal">PATH_TRANSLATED</tt>.)

A WSGI-compliant server or gateway **should** document what variables
it provides, along with their definitions as appropriate.  Applications
**should** check for the presence of any variables they require, and
have a fallback plan in the event such a variable is absent.

Note: missing variables (such as <tt class="docutils literal">REMOTE_USER</tt> when no
authentication has occurred) should be left out of the <tt class="docutils literal">environ</tt>
dictionary.  Also note that CGI-defined variables must be native strings,
if they are present at all.  It is a violation of this specification
for _any_ CGI variable's value to be of any type other than <tt class="docutils literal">str</tt>.

In addition to the CGI-defined variables, the <tt class="docutils literal">environ</tt> dictionary
**may** also contain arbitrary operating-system "environment variables",
and **must** contain the following WSGI-defined variables:

<table border="1" class="docutils">
<colgroup>
<col width="28%">
<col width="72%">
</colgroup>
<thead valign="bottom">
<tr><th class="head">Variable</th>
<th class="head">Value</th>
</tr>
</thead>
<tbody valign="top">
<tr><td><tt class="docutils literal">wsgi.version</tt></td>
<td>The tuple <tt class="docutils literal">(1, 0)</tt>, representing WSGI
version 1.0.</td>
</tr>
<tr><td><tt class="docutils literal">wsgi.url_scheme</tt></td>
<td>A string representing the "scheme" portion of
the URL at which the application is being
invoked.  Normally, this will have the value
<tt class="docutils literal">"http"</tt> or <tt class="docutils literal">"https"</tt>, as appropriate.</td>
</tr>
<tr><td><tt class="docutils literal">wsgi.input</tt></td>
<td>An input stream (file-like object) from which
the HTTP request body bytes can be read.  (The server
or gateway may perform reads on-demand as
requested by the application, or it may pre-
read the client's request body and buffer it
in-memory or on disk, or use any other
technique for providing such an input stream,
according to its preference.)</td>
</tr>
<tr><td><tt class="docutils literal">wsgi.errors</tt></td>
<td>

An output stream (file-like object) to which
error output can be written, for the purpose of
recording program or other errors in a
standardized and possibly centralized location.
This should be a "text mode" stream; i.e.,
applications should use <tt class="docutils literal">"\n"</tt> as a line
ending, and assume that it will be converted to
the correct line ending by the server/gateway.

(On platforms where the <tt class="docutils literal">str</tt> type is unicode,
the error stream **should** accept and log
arbitary unicode without raising an error; it
is allowed, however, to substitute characters
that cannot be rendered in the stream's encoding.)

For many servers, <tt class="docutils literal">wsgi.errors</tt> will be the
server's main error log. Alternatively, this
may be <tt class="docutils literal">sys.stderr</tt>, or a log file of some
sort.  The server's documentation should
include an explanation of how to configure this
or where to find the recorded output.  A server
or gateway may supply different error streams
to different applications, if this is desired.

</td>
</tr>
<tr><td><tt class="docutils literal">wsgi.multithread</tt></td>
<td>This value should evaluate true if the
application object may be simultaneously
invoked by another thread in the same process,
and should evaluate false otherwise.</td>
</tr>
<tr><td><tt class="docutils literal">wsgi.multiprocess</tt></td>
<td>This value should evaluate true if an
equivalent application object may be
simultaneously invoked by another process,
and should evaluate false otherwise.</td>
</tr>
<tr><td><tt class="docutils literal">wsgi.run_once</tt></td>
<td>This value should evaluate true if the server
or gateway expects (but does not guarantee!)
that the application will only be invoked this
one time during the life of its containing
process.  Normally, this will only be true for
a gateway based on CGI (or something similar).</td>
</tr>
</tbody>
</table>

Finally, the <tt class="docutils literal">environ</tt> dictionary may also contain server-defined
variables.  These variables should be named using only lower-case
letters, numbers, dots, and underscores, and should be prefixed with
a name that is unique to the defining server or gateway.  For
example, <tt class="docutils literal">mod_python</tt> might define variables with names like
<tt class="docutils literal">mod_python.some_variable</tt>.