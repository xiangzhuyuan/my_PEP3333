# [Proposed/Under Discussion](#id43)

These items are currently being discussed on the Web-SIG and elsewhere,
or are on the PEP author's "to-do" list:

*   Should <tt class="docutils literal">wsgi.input</tt> be an iterator instead of a file?  This would
help for asynchronous applications and chunked-encoding input
streams.
*   Optional extensions are being discussed for pausing iteration of an
application's output until input is available or until a callback
occurs.
*   Add a section about synchronous vs. asynchronous apps and servers,
the relevant threading models, and issues/design goals in these
areas.
