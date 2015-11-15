## [Other HTTP Features](#id34)

In general, servers and gateways should "play dumb" and allow the
application complete control over its output.  They should only make
changes that do not alter the effective semantics of the application's
response.  It is always possible for the application developer to add
middleware components to supply additional features, so server/gateway
developers should be conservative in their implementation.  In a sense,
a server should consider itself to be like an HTTP "gateway server",
with the application being an HTTP "origin server".  (See [RFC 2616](http://www.faqs.org/rfcs/rfc2616.html),
section 1.3, for the definition of these terms.)

However, because WSGI servers and applications do not communicate via
HTTP, what [RFC 2616](http://www.faqs.org/rfcs/rfc2616.html) calls "hop-by-hop" headers do not apply to WSGI
internal communications.  WSGI applications **must not** generate any
"hop-by-hop" headers [[4]](#id11), attempt to use HTTP features that would
require them to generate such headers, or rely on the content of
any incoming "hop-by-hop" headers in the <tt class="docutils literal">environ</tt> dictionary.
WSGI servers **must** handle any supported inbound "hop-by-hop" headers
on their own, such as by decoding any inbound <tt class="docutils literal"><span class="pre">Transfer-Encoding</span></tt>,
including chunked encoding if applicable.

Applying these principles to a variety of HTTP features, it should be
clear that a server **may** handle cache validation via the
<tt class="docutils literal"><span class="pre">If-None-Match</span></tt> and <tt class="docutils literal"><span class="pre">If-Modified-Since</span></tt> request headers and the
<tt class="docutils literal"><span class="pre">Last-Modified</span></tt> and <tt class="docutils literal">ETag</tt> response headers.  However, it is
not required to do this, and the application **should** perform its
own cache validation if it wants to support that feature, since
the server/gateway is not required to do such validation.

Similarly, a server **may** re-encode or transport-encode an
application's response, but the application **should** use a
suitable content encoding on its own, and **must not** apply a
transport encoding.  A server **may** transmit byte ranges of the
application's response if requested by the client, and the
application doesn't natively support byte ranges.  Again, however,
the application **should** perform this function on its own if desired.

Note that these restrictions on applications do not necessarily mean
that every application must reimplement every HTTP feature; many HTTP
features can be partially or fully implemented by middleware
components, thus freeing both server and application authors from
implementing the same features over and over again.
