## 应用/框架 端
一个应用对象就是一个可以被调用的对象,这个对象的定义,不应该看做是一个实际的对象实例,一个函数,一个方法,
类?或者一个有<tt class="docutils literal">__call__</tt>方法的实例,他们都是可以被接受的,作为一个应用对象.

应用对象必须能够调用多次,因为所谓服务器和网关都会被多次调用.
(注意:虽然我们称之为应用对象,但并不是意味着应用程序开发人员要使用wSGI作为一个web编程的api.但是还是要使用那些个更加高级的
api,WSGI是一个工具被用来开发server或者框架的人员的使用的.而并非共工程师所用)

下面是两个例子,演示了应用对象,一个是一个函数,一个是类!

<pre class="literal-block">HELLO_WORLD = b"Hello world!\n"

def simple_app(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [HELLO_WORLD]

class AppClass:
    """Produce the same output, but using a class

    (Note: 'AppClass' is the "application" here, so calling it
    returns an instance of 'AppClass', which is then the iterable
    return value of the "application callable" as required by
    the spec.

    If we wanted to use *instances* of 'AppClass' as application
    objects instead, we would have to implement a '__call__'
    method, which would be invoked to execute the application,
    and we would need to create an instance for use by the
    server or gateway.
    """

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response

    def __iter__(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield HELLO_WORLD
</pre>