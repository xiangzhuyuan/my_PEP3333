### [Handling the <tt class="docutils literal"><span class="pre">Content-Length</span></tt> Header](#id27)

If the application supplies a <tt class="docutils literal"><span class="pre">Content-Length</span></tt> header, the server
**should not** transmit more bytes to the client than the header
allows, and **should** stop iterating over the response when enough
data has been sent, or raise an error if the application tries to
<tt class="docutils literal">write()</tt> past that point.  (Of course, if the application does
not provide _enough_ data to meet its stated <tt class="docutils literal"><span class="pre">Content-Length</span></tt>,
the server **should** close the connection and log or otherwise
report the error.)

If the application does not supply a <tt class="docutils literal"><span class="pre">Content-Length</span></tt> header, a
server or gateway may choose one of several approaches to handling
it.  The simplest of these is to close the client connection when
the response is completed.

Under some circumstances, however, the server or gateway may be
able to either generate a <tt class="docutils literal"><span class="pre">Content-Length</span></tt> header, or at least
avoid the need to close the client connection.  If the application
does _not_ call the <tt class="docutils literal">write()</tt> callable, and returns an iterable
whose <tt class="docutils literal">len()</tt> is 1, then the server can automatically determine
<tt class="docutils literal"><span class="pre">Content-Length</span></tt> by taking the length of the first bytestring yielded
by the iterable.

And, if the server and client both support HTTP/1.1 "chunked
encoding" [[3]](#id10), then the server **may** use chunked encoding to send
a chunk for each <tt class="docutils literal">write()</tt> call or bytestring yielded by the iterable,
thus generating a <tt class="docutils literal"><span class="pre">Content-Length</span></tt> header for each chunk.  This
allows the server to keep the client connection alive, if it wishes
to do so.  Note that the server **must** comply fully with [RFC 2616](http://www.faqs.org/rfcs/rfc2616.html)
when doing this, or else fall back to one of the other strategies for
dealing with the absence of <tt class="docutils literal"><span class="pre">Content-Length</span></tt>.

(Note: applications and middleware **must not** apply any kind of
<tt class="docutils literal"><span class="pre">Transfer-Encoding</span></tt> to their output, such as chunking or gzipping;
as "hop-by-hop" operations, these encodings are the province of the
actual web server/gateway.  See [Other HTTP Features](#other-http-features) below, for
more details.)