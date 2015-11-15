# 中间件,脚踩2只船的角色

其实中间件对于服务器端或者应用端都是一点关系.也就是所谓的中间件吧!
比如:

* 路由一个请求到正确的应用对象,基于给定的url.通过重写<tt class="docutils literal">environ</tt>.
* 可以让多个不用的应用或者框架前后同时跑在同一个进程中.
* 负载均衡和远程处理,分发请求和响应在网络上.
* 处理文本内容,例如分析XSL样式.

一般来说,中间件对于服务器端和应用端都是透明的,不应该有额外的一些需要支持,

用户谁想要把中间件到应用程序中简单提供中间件组件到服务器，就好像它是
一个应用程序，并配置中间件组件调用应用程序，仿佛中间件组件是一个服务器。
当然，在“应用程序” ，该中间件包裹实际上可能是另一个中间件组件包裹另一个
应用，等等，产生什么被称为“中间件堆栈” 。

在大多数情况下，中间件必须符合限制与服务器和应用程序的边要求WSGI 。
在某些情况下，然而，需要对中间件是不是一个“纯粹”的服务器或应用程序更加严格，
这些点可以注意到在本说明书中。

这是一个简单的例子,关于中间组件的,转化<tt class="docutils literal">text/plain</tt> 到响应,使用
<tt class="docutils literal">piglatin.py</tt>.注意,一个'真'的中间组件将会使用一个更加机械的方式来验证
内容文本,同时这个简单例子忽略了一个可能性,就是一个单词可能会被分割开来.

<pre class="literal-block">
from piglatin import piglatin

class LatinIter:

    """Transform iterated output to piglatin, if it's okay to do so

    Note that the "okayness" can change until the application yields
    its first non-empty bytestring, so 'transform_ok' has to be a mutable
    truth value.
    """

    def __init__(self, result, transform_ok):
        if hasattr(result, 'close'):
            self.close = result.close
        self._next = iter(result).__next__
        self.transform_ok = transform_ok

    def __iter__(self):
        return self

    def __next__(self):
        if self.transform_ok:
            return piglatin(self._next())   # call must be byte-safe on Py3
        else:
            return self._next()

class Latinator:

    # by default, don't transform output
    transform = False

    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):

        transform_ok = []

        def start_latin(status, response_headers, exc_info=None):

            # Reset ok flag, in case this is a repeat call
            del transform_ok[:]

            for name, value in response_headers:
                if name.lower() == 'content-type' and value == 'text/plain':
                    transform_ok.append(True)
                    # Strip content-length if present, else it'll be wrong
                    response_headers = [(name, value)
                        for name, value in response_headers
                            if name.lower() != 'content-length'
                    ]
                    break

            write = start_response(status, response_headers, exc_info)

            if transform_ok:
                def write_latin(data):
                    write(piglatin(data))   # call must be byte-safe on Py3
                return write_latin
            else:
                return write

        return LatinIter(self.application(environ, start_latin), transform_ok)

# Run foo_app under a Latinator's control, using the example CGI gateway
from foo_app import foo_app
run_with_cgi(Latinator(foo_app))
</pre>