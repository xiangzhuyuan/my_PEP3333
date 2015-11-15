## [HTTP 1.1 Expect/Continue](#id33)

Servers and gateways that implement HTTP 1.1 **must** provide
transparent support for HTTP 1.1's "expect/continue" mechanism.  This
may be done in any of several ways:

1.  Respond to requests containing an <tt class="docutils literal">Expect: <span class="pre">100-continue</span></tt> request
with an immediate "100 Continue" response, and proceed normally.
2.  Proceed with the request normally, but provide the application
with a <tt class="docutils literal">wsgi.input</tt> stream that will send the "100 Continue"
response if/when the application first attempts to read from the
input stream.  The read request must then remain blocked until the
client responds.
3.  Wait until the client decides that the server does not support
expect/continue, and sends the request body on its own.  (This
is suboptimal, and is not recommended.)

Note that these behavior restrictions do not apply for HTTP 1.0
requests, or for requests that are not directed to an application
object.  For more information on HTTP 1.1 Expect/Continue, see [RFC
2616](http://www.faqs.org/rfcs/rfc2616.html), sections 8.2.3 and 10.1.1.