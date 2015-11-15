### [Input and Error Streams](#id25)

The input and error streams provided by the server must support
the following methods:

<table border="1" class="docutils">
<colgroup>
<col width="51%">
<col width="27%">
<col width="22%">
</colgroup>
<thead valign="bottom">
<tr><th class="head">Method</th>
<th class="head">Stream</th>
<th class="head">Notes</th>
</tr>
</thead>
<tbody valign="top">
<tr><td><tt class="docutils literal">read(size)</tt></td>
<td><tt class="docutils literal">input</tt></td>
<td>1</td>
</tr>
<tr><td><tt class="docutils literal">readline()</tt></td>
<td><tt class="docutils literal">input</tt></td>
<td>1, 2</td>
</tr>
<tr><td><tt class="docutils literal">readlines(hint)</tt></td>
<td><tt class="docutils literal">input</tt></td>
<td>1, 3</td>
</tr>
<tr><td><tt class="docutils literal">__iter__()</tt></td>
<td><tt class="docutils literal">input</tt></td>
<td>&nbsp;</td>
</tr>
<tr><td><tt class="docutils literal">flush()</tt></td>
<td><tt class="docutils literal">errors</tt></td>
<td>4</td>
</tr>
<tr><td><tt class="docutils literal">write(str)</tt></td>
<td><tt class="docutils literal">errors</tt></td>
<td>&nbsp;</td>
</tr>
<tr><td><tt class="docutils literal">writelines(seq)</tt></td>
<td><tt class="docutils literal">errors</tt></td>
<td>&nbsp;</td>
</tr>
</tbody>
</table>

The semantics of each method are as documented in the Python Library
Reference, except for these notes as listed in the table above:

1.  The server is not required to read past the client's specified
<tt class="docutils literal"><span class="pre">Content-Length</span></tt>, and **should** simulate an end-of-file
condition if the application attempts to read past that point.
The application **should not** attempt to read more data than is
specified by the <tt class="docutils literal">CONTENT_LENGTH</tt> variable.

    A server **should** allow <tt class="docutils literal">read()</tt> to be called without an argument,
and return the remainder of the client's input stream.

    A server **should** return empty bytestrings from any attempt to
read from an empty or exhausted input stream.

2.  Servers **should** support the optional "size" argument to <tt class="docutils literal">readline()</tt>,
but as in WSGI 1.0, they are allowed to omit support for it.

    (In WSGI 1.0, the size argument was not supported, on the grounds that
it might have been complex to implement, and was not often used in
practice...  but then the <tt class="docutils literal">cgi</tt> module started using it, and so
practical servers had to start supporting it anyway!)

3.  Note that the <tt class="docutils literal">hint</tt> argument to <tt class="docutils literal">readlines()</tt> is optional for
both caller and implementer.  The application is free not to
supply it, and the server or gateway is free to ignore it.

4.  Since the <tt class="docutils literal">errors</tt> stream may not be rewound, servers and gateways
are free to forward write operations immediately, without buffering.
In this case, the <tt class="docutils literal">flush()</tt> method may be a no-op.  Portable
applications, however, cannot assume that output is unbuffered
or that <tt class="docutils literal">flush()</tt> is a no-op.  They must call <tt class="docutils literal">flush()</tt> if
they need to ensure that output has in fact been written.  (For
example, to minimize intermingling of data from multiple processes
writing to the same error log.)

The methods listed in the table above **must** be supported by all
servers conforming to this specification.  Applications conforming
to this specification **must not** use any other methods or attributes
of the <tt class="docutils literal">input</tt> or <tt class="docutils literal">errors</tt> objects.  In particular, applications
**must not** attempt to close these streams, even if they possess
<tt class="docutils literal">close()</tt> methods.