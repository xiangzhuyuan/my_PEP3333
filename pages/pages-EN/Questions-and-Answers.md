# [Questions and Answers](#id42)

1.  Why must <tt class="docutils literal">environ</tt> be a dictionary?  What's wrong with using a
subclass?

    The rationale for requiring a dictionary is to maximize portability
between servers.  The alternative would be to define some subset of
a dictionary's methods as being the standard and portable
interface.  In practice, however, most servers will probably find a
dictionary adequate to their needs, and thus framework authors will
come to expect the full set of dictionary features to be available,
since they will be there more often than not.  But, if some server
chooses _not_ to use a dictionary, then there will be
interoperability problems despite that server's "conformance" to
spec.  Therefore, making a dictionary mandatory simplifies the
specification and guarantees interoperabilty.

    Note that this does not prevent server or framework developers from
offering specialized services as custom variables _inside_ the
<tt class="docutils literal">environ</tt> dictionary.  This is the recommended approach for
offering any such value-added services.

2.  Why can you call <tt class="docutils literal">write()</tt> _and_ yield bytestrings/return an
iterable?  Shouldn't we pick just one way?

    If we supported only the iteration approach, then current
frameworks that assume the availability of "push" suffer.  But, if
we only support pushing via <tt class="docutils literal">write()</tt>, then server performance
suffers for transmission of e.g. large files (if a worker thread
can't begin work on a new request until all of the output has been
sent).  Thus, this compromise allows an application framework to
support both approaches, as appropriate, but with only a little
more burden to the server implementor than a push-only approach
would require.

3.  What's the <tt class="docutils literal">close()</tt> for?

    When writes are done during the execution of an application
object, the application can ensure that resources are released
using a try/finally block.  But, if the application returns an
iterable, any resources used will not be released until the
iterable is garbage collected.  The <tt class="docutils literal">close()</tt> idiom allows an
application to release critical resources at the end of a request,
and it's forward-compatible with the support for try/finally in
generators that's proposed by [PEP 325](/dev/peps/pep-0325).

4.  Why is this interface so low-level?  I want feature X!  (e.g.
cookies, sessions, persistence, ...)

    This isn't Yet Another Python Web Framework.  It's just a way for
frameworks to talk to web servers, and vice versa.  If you want
these features, you need to pick a web framework that provides the
features you want.  And if that framework lets you create a WSGI
application, you should be able to run it in most WSGI-supporting
servers.  Also, some WSGI servers may offer additional services via
objects provided in their <tt class="docutils literal">environ</tt> dictionary; see the
applicable server documentation for details.  (Of course,
applications that use such extensions will not be portable to other
WSGI-based servers.)

5.  Why use CGI variables instead of good old HTTP headers?  And why
mix them in with WSGI-defined variables?

    Many existing web frameworks are built heavily upon the CGI spec,
and existing web servers know how to generate CGI variables.  In
contrast, alternative ways of representing inbound HTTP information
are fragmented and lack market share.  Thus, using the CGI
"standard" seems like a good way to leverage existing
implementations.  As for mixing them with WSGI variables,
separating them would just require two dictionary arguments to be
passed around, while providing no real benefits.

6.  What about the status string?  Can't we just use the number,
passing in <tt class="docutils literal">200</tt> instead of <tt class="docutils literal">"200 OK"</tt>?

    Doing this would complicate the server or gateway, by requiring
them to have a table of numeric statuses and corresponding
messages.  By contrast, it is easy for an application or framework
author to type the extra text to go with the specific response code
they are using, and existing frameworks often already have a table
containing the needed messages.  So, on balance it seems better to
make the application/framework responsible, rather than the server
or gateway.

7.  Why is <tt class="docutils literal">wsgi.run_once</tt> not guaranteed to run the app only once?

    Because it's merely a suggestion to the application that it should
"rig for infrequent running".  This is intended for application
frameworks that have multiple modes of operation for caching,
sessions, and so forth.  In a "multiple run" mode, such frameworks
may preload caches, and may not write e.g. logs or session data to
disk after each request.  In "single run" mode, such frameworks
avoid preloading and flush all necessary writes after each request.

    However, in order to test an application or framework to verify
correct operation in the latter mode, it may be necessary (or at
least expedient) to invoke it more than once.  Therefore, an
application should not assume that it will definitely not be run
again, just because it is called with <tt class="docutils literal">wsgi.run_once</tt> set to
<tt class="docutils literal">True</tt>.

8.  Feature X (dictionaries, callables, etc.) are ugly for use in
application code; why don't we use objects instead?

    All of these implementation choices of WSGI are specifically
intended to _decouple_ features from one another; recombining these
features into encapsulated objects makes it somewhat harder to
write servers or gateways, and an order of magnitude harder to
write middleware that replaces or modifies only small portions of
the overall functionality.

    In essence, middleware wants to have a "Chain of Responsibility"
pattern, whereby it can act as a "handler" for some functions,
while allowing others to remain unchanged.  This is difficult to do
with ordinary Python objects, if the interface is to remain
extensible.  For example, one must use <tt class="docutils literal">__getattr__</tt> or
<tt class="docutils literal">__getattribute__</tt> overrides, to ensure that extensions (such as
attributes defined by future WSGI versions) are passed through.

    This type of code is notoriously difficult to get 100% correct, and
few people will want to write it themselves.  They will therefore
copy other people's implementations, but fail to update them when
the person they copied from corrects yet another corner case.

    Further, this necessary boilerplate would be pure excise, a
developer tax paid by middleware developers to support a slightly
prettier API for application framework developers.  But,
application framework developers will typically only be updating
_one_ framework to support WSGI, and in a very limited part of
their framework as a whole.  It will likely be their first (and
maybe their only) WSGI implementation, and thus they will likely
implement with this specification ready to hand.  Thus, the effort
of making the API "prettier" with object attributes and suchlike
would likely be wasted for this audience.

    We encourage those who want a prettier (or otherwise improved) WSGI
interface for use in direct web application programming (as opposed
to web framework development) to develop APIs or frameworks that
wrap WSGI for convenient use by application developers.  In this
way, WSGI can remain conveniently low-level for server and
middleware authors, while not being "ugly" for application
developers.
