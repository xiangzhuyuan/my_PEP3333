# [Acknowledgements](#id44)

Thanks go to the many folks on the Web-SIG mailing list whose
thoughtful feedback made this revised draft possible.  Especially:

*   Gregory "Grisha" Trubetskoy, author of <tt class="docutils literal">mod_python</tt>, who beat up
on the first draft as not offering any advantages over "plain old
CGI", thus encouraging me to look for a better approach.
*   Ian Bicking, who helped nag me into properly specifying the
multithreading and multiprocess options, as well as badgering me to
provide a mechanism for servers to supply custom extension data to
an application.
*   Tony Lownds, who came up with the concept of a <tt class="docutils literal">start_response</tt>
function that took the status and headers, returning a <tt class="docutils literal">write</tt>
function.  His input also guided the design of the exception handling
facilities, especially in the area of allowing for middleware that
overrides application error messages.
*   Alan Kennedy, whose courageous attempts to implement WSGI-on-Jython
(well before the spec was finalized) helped to shape the "supporting
older versions of Python" section, as well as the optional
<tt class="docutils literal">wsgi.file_wrapper</tt> facility, and some of the early bytes/unicode
decisions.
*   Mark Nottingham, who reviewed the spec extensively for issues with
HTTP RFC compliance, especially with regard to HTTP/1.1 features that
I didn't even know existed until he pointed them out.
*   Graham Dumpleton, who worked tirelessly (even in the face of my laziness
and stupidity) to get some sort of Python 3 version of WSGI out, who
proposed the "native strings" vs. "byte strings" concept, and thoughtfully
wrestled through a great many HTTP, <tt class="docutils literal">wsgi.input</tt>, and other
amendments.  Most, if not all, of the credit for this new PEP
belongs to him.
