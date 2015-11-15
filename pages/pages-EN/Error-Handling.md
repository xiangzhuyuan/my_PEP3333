## [Error Handling](#id32)

In general, applications **should** try to trap their own, internal
errors, and display a helpful message in the browser.  (It is up
to the application to decide what "helpful" means in this context.)

However, to display such a message, the application must not have
actually sent any data to the browser yet, or else it risks corrupting
the response.  WSGI therefore provides a mechanism to either allow the
application to send its error message, or be automatically aborted:
the <tt class="docutils literal">exc_info</tt> argument to <tt class="docutils literal">start_response</tt>.  Here is an example
of its use:

<pre class="literal-block">try:
    # regular application code here
    status = "200 Froody"
    response_headers = [("content-type", "text/plain")]
    start_response(status, response_headers)
    return ["normal body goes here"]
except:
    # XXX should trap runtime issues like MemoryError, KeyboardInterrupt
    #     in a separate handler before this bare 'except:'...
    status = "500 Oops"
    response_headers = [("content-type", "text/plain")]
    start_response(status, response_headers, sys.exc_info())
    return ["error body goes here"]
</pre>

If no output has been written when an exception occurs, the call to
<tt class="docutils literal">start_response</tt> will return normally, and the application will
return an error body to be sent to the browser.  However, if any output
has already been sent to the browser, <tt class="docutils literal">start_response</tt> will reraise
the provided exception.  This exception **should not** be trapped by
the application, and so the application will abort.  The server or
gateway can then trap this (fatal) exception and abort the response.

Servers **should** trap and log any exception that aborts an
application or the iteration of its return value.  If a partial
response has already been written to the browser when an application
error occurs, the server or gateway **may** attempt to add an error
message to the output, if the already-sent headers indicate a
<tt class="docutils literal">text/*</tt> content type that the server knows how to modify cleanly.

Some middleware may wish to provide additional exception handling
services, or intercept and replace application error messages.  In
such cases, middleware may choose to **not** re-raise the <tt class="docutils literal">exc_info</tt>
supplied to <tt class="docutils literal">start_response</tt>, but instead raise a middleware-specific
exception, or simply return without an exception after storing the
supplied arguments.  This will then cause the application to return
its error body iterable (or invoke <tt class="docutils literal">write()</tt>), allowing the middleware
to capture and modify the error output.  These techniques will work as
long as application authors:

1.  Always provide <tt class="docutils literal">exc_info</tt> when beginning an error response
2.  Never trap errors raised by <tt class="docutils literal">start_response</tt> when <tt class="docutils literal">exc_info</tt> is
being provided