## [Application Configuration](#id38)

This specification does not define how a server selects or obtains an
application to invoke.  These and other configuration options are
highly server-specific matters.  It is expected that server/gateway
authors will document how to configure the server to execute a
particular application object, and with what options (such as
threading options).

Framework authors, on the other hand, should document how to create an
application object that wraps their framework's functionality.  The
user, who has chosen both the server and the application framework,
must connect the two together.  However, since both the framework and
the server now have a common interface, this should be merely a
mechanical matter, rather than a significant engineering effort for
each new server/framework pair.

Finally, some applications, frameworks, and middleware may wish to
use the <tt class="docutils literal">environ</tt> dictionary to receive simple string configuration
options.  Servers and gateways **should** support this by allowing
an application's deployer to specify name-value pairs to be placed in
<tt class="docutils literal">environ</tt>.  In the simplest case, this support can consist merely of
copying all operating system-supplied environment variables from
<tt class="docutils literal">os.environ</tt> into the <tt class="docutils literal">environ</tt> dictionary, since the deployer in
principle can configure these externally to the server, or in the
CGI case they may be able to be set via the server's configuration
files.

Applications **should** try to keep such required variables to a
minimum, since not all servers will support easy configuration of
them.  Of course, even in the worst case, persons deploying an
application can create a script to supply the necessary configuration
values:

<pre class="literal-block">from the_app import application

def new_app(environ, start_response):
    environ['the_app.configval1'] = 'something'
    return application(environ, start_response)
</pre>

But, most existing applications and frameworks will probably only need
a single configuration value from <tt class="docutils literal">environ</tt>, to indicate the location
of their application or framework-specific configuration file(s).  (Of
course, applications should cache such configuration, to avoid having
to re-read it upon each invocation.)