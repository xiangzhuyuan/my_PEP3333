### [The <tt class="docutils literal">write()</tt> Callable](#id30)

Some existing application framework APIs support unbuffered
output in a different manner than WSGI.  Specifically, they
provide a "write" function or method of some kind to write
an unbuffered block of data, or else they provide a buffered
"write" function and a "flush" mechanism to flush the buffer.

Unfortunately, such APIs cannot be implemented in terms of
WSGI's "iterable" application return value, unless threads
or other special mechanisms are used.

Therefore, to allow these frameworks to continue using an
imperative API, WSGI includes a special <tt class="docutils literal">write()</tt> callable,
returned by the <tt class="docutils literal">start_response</tt> callable.

New WSGI applications and frameworks **should not** use the
<tt class="docutils literal">write()</tt> callable if it is possible to avoid doing so.  The
<tt class="docutils literal">write()</tt> callable is strictly a hack to support imperative
streaming APIs.  In general, applications should produce their
output via their returned iterable, as this makes it possible
for web servers to interleave other tasks in the same Python thread,
potentially providing better throughput for the server as a whole.

The <tt class="docutils literal">write()</tt> callable is returned by the <tt class="docutils literal">start_response()</tt>
callable, and it accepts a single parameter:  a bytestring to be
written as part of the HTTP response body, that is treated exactly
as though it had been yielded by the output iterable.  In other
words, before <tt class="docutils literal">write()</tt> returns, it must guarantee that the
passed-in bytestring was either completely sent to the client, or
that it is buffered for transmission while the application
proceeds onward.

An application **must** return an iterable object, even if it
uses <tt class="docutils literal">write()</tt> to produce all or part of its response body.
The returned iterable **may** be empty (i.e. yield no non-empty
bytestrings), but if it _does_ yield non-empty bytestrings, that output
must be treated normally by the server or gateway (i.e., it must be
sent or queued immediately).  Applications **must not** invoke
<tt class="docutils literal">write()</tt> from within their return iterable, and therefore any
bytestrings yielded by the iterable are transmitted after all bytestrings
passed to <tt class="docutils literal">write()</tt> have been sent to the client.