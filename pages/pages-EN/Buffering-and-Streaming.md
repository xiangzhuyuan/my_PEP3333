## [Buffering and Streaming](#id28)

Generally speaking, applications will achieve the best throughput
by buffering their (modestly-sized) output and sending it all at
once.  This is a common approach in existing frameworks such as
Zope: the output is buffered in a StringIO or similar object, then
transmitted all at once, along with the response headers.

The corresponding approach in WSGI is for the application to simply
return a single-element iterable (such as a list) containing the
response body as a single bytestring.  This is the recommended approach
for the vast majority of application functions, that render
HTML pages whose text easily fits in memory.

For large files, however, or for specialized uses of HTTP streaming
(such as multipart "server push"), an application may need to provide
output in smaller blocks (e.g. to avoid loading a large file into
memory).  It's also sometimes the case that part of a response may
be time-consuming to produce, but it would be useful to send ahead the
portion of the response that precedes it.

In these cases, applications will usually return an iterator (often
a generator-iterator) that produces the output in a block-by-block
fashion.  These blocks may be broken to coincide with mulitpart
boundaries (for "server push"), or just before time-consuming
tasks (such as reading another block of an on-disk file).

WSGI servers, gateways, and middleware **must not** delay the
transmission of any block; they **must** either fully transmit
the block to the client, or guarantee that they will continue
transmission even while the application is producing its next block.
A server/gateway or middleware may provide this guarantee in one of
three ways:

1.  Send the entire block to the operating system (and request
that any O/S buffers be flushed) before returning control
to the application, OR
2.  Use a different thread to ensure that the block continues
to be transmitted while the application produces the next
block.
3.  (Middleware only) send the entire block to its parent
gateway/server

By providing this guarantee, WSGI allows applications to ensure
that transmission will not become stalled at an arbitrary point
in their output data.  This is critical for proper functioning
of e.g. multipart "server push" streaming, where data between
multipart boundaries should be transmitted in full to the client.