# [Preface for Readers of PEP 333](#id15)

This is an updated version of [PEP 333](/dev/peps/pep-0333), modified slightly to improve
usability under Python 3, and to incorporate several long-standing
de-facto amendments to the WSGI protocol.  (Its code samples have
also been ported to Python 3.)

While for procedural reasons [[6]](#id13), this must be a distinct PEP, no
changes were made that invalidate previously-compliant servers or
applications under Python 2.x.  If your 2.x application or server
is compliant to PEP 333, it is also compliant with this PEP.

Under Python 3, however, your app or server must also follow the
rules outlined in the sections below titled, [A Note On String
Types](#a-note-on-string-types), and [Unicode Issues](#unicode-issues).

For detailed, line-by-line diffs between this document and PEP 333,
you may view its SVN revision history [[7]](#id14), from revision 84854 forward.