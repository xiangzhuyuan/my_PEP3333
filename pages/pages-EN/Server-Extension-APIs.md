## [Server Extension APIs](#id37)

Some server authors may wish to expose more advanced APIs, that
application or framework authors can use for specialized purposes.
For example, a gateway based on <tt class="docutils literal">mod_python</tt> might wish to expose
part of the Apache API as a WSGI extension.

In the simplest case, this requires nothing more than defining an
<tt class="docutils literal">environ</tt> variable, such as <tt class="docutils literal">mod_python.some_api</tt>.  But, in many
cases, the possible presence of middleware can make this difficult.
For example, an API that offers access to the same HTTP headers that
are found in <tt class="docutils literal">environ</tt> variables, might return different data if
<tt class="docutils literal">environ</tt> has been modified by middleware.

In general, any extension API that duplicates, supplants, or bypasses
some portion of WSGI functionality runs the risk of being incompatible
with middleware components.  Server/gateway developers should _not_
assume that nobody will use middleware, because some framework
developers specifically intend to organize or reorganize their
frameworks to function almost entirely as middleware of various kinds.

So, to provide maximum compatibility, servers and gateways that
provide extension APIs that replace some WSGI functionality, **must**
design those APIs so that they are invoked using the portion of the
API that they replace.  For example, an extension API to access HTTP
request headers must require the application to pass in its current
<tt class="docutils literal">environ</tt>, so that the server/gateway may verify that HTTP headers
accessible via the API have not been altered by middleware.  If the
extension API cannot guarantee that it will always agree with
<tt class="docutils literal">environ</tt> about the contents of HTTP headers, it must refuse service
to the application, e.g. by raising an error, returning <tt class="docutils literal">None</tt>
instead of a header collection, or whatever is appropriate to the API.

Similarly, if an extension API provides an alternate means of writing
response data or headers, it should require the <tt class="docutils literal">start_response</tt>
callable to be passed in, before the application can obtain the
extended service.  If the object passed in is not the same one that
the server/gateway originally supplied to the application, it cannot
guarantee correct operation and must refuse to provide the extended
service to the application.

These guidelines also apply to middleware that adds information such
as parsed cookies, form variables, sessions, and the like to
<tt class="docutils literal">environ</tt>.  Specifically, such middleware should provide these
features as functions which operate on <tt class="docutils literal">environ</tt>, rather than simply
stuffing values into <tt class="docutils literal">environ</tt>.  This helps ensure that information
is calculated from <tt class="docutils literal">environ</tt> _after_ any middleware has done any URL
rewrites or other <tt class="docutils literal">environ</tt> modifications.

It is very important that these "safe extension" rules be followed by
both server/gateway and middleware developers, in order to avoid a
future in which middleware developers are forced to delete any and all
extension APIs from <tt class="docutils literal">environ</tt> to ensure that their mediation isn't
being bypassed by applications using those extensions!
