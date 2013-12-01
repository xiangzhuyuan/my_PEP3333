### [Middleware Handling of Block Boundaries](#id29)

In order to better support asynchronous applications and servers,
middleware components **must not** block iteration waiting for
multiple values from an application iterable.  If the middleware
needs to accumulate more data from the application before it can
produce any output, it **must** yield an empty bytestring.

To put this requirement another way, a middleware component **must
yield at least one value** each time its underlying application
yields a value.  If the middleware cannot yield any other value,
it must yield an empty bytestring.

This requirement ensures that asynchronous applications and servers
can conspire to reduce the number of threads that are required
to run a given number of application instances simultaneously.

Note also that this requirement means that middleware **must**
return an iterable as soon as its underlying application returns
an iterable.  It is also forbidden for middleware to use the
<tt class="docutils literal">write()</tt> callable to transmit data that is yielded by an
underlying application.  Middleware may only use their parent
server's <tt class="docutils literal">write()</tt> callable to transmit data that the
underlying application sent using a middleware-provided <tt class="docutils literal">write()</tt>
callable.