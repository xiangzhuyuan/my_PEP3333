## [URL Reconstruction](#id39)

If an application wishes to reconstruct a request's complete URL, it
may do so using the following algorithm, contributed by Ian Bicking:

<pre class="literal-block">from urllib import quote
url = environ['wsgi.url_scheme']+'://'

if environ.get('HTTP_HOST'):
    url += environ['HTTP_HOST']
else:
    url += environ['SERVER_NAME']

    if environ['wsgi.url_scheme'] == 'https':
        if environ['SERVER_PORT'] != '443':
           url += ':' + environ['SERVER_PORT']
    else:
        if environ['SERVER_PORT'] != '80':
           url += ':' + environ['SERVER_PORT']

url += quote(environ.get('SCRIPT_NAME', ''))
url += quote(environ.get('PATH_INFO', ''))
if environ.get('QUERY_STRING'):
    url += '?' + environ['QUERY_STRING']
</pre>

Note that such a reconstructed URL may not be precisely the same URI
as requested by the client.  Server rewrite rules, for example, may
have modified the client's originally requested URL to place it in a
canonical form.