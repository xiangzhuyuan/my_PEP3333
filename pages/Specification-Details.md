# 定义详细

应用对象必须有两个参数,这个参数是位置型的,为了便于演示,我们命名为
<tt class="docutils literal">environ</tt> 和
<tt class="docutils literal">start_response</tt>,但是他们也不是必须起这个名字.
一个server或者网关 **必须** 请求这个应用对象通过位置参数.例如,通过呼叫
<tt class="docutils literal">result = application(environ, start_response)</tt>
来实现.


这个<tt class="docutils literal">environ</tt>参数是一个字典对象,包含类CGI环境的所有
变量,这个对象 **必须** 是Python内建的一个字典类型,(不能够是用户实现的子类等).

能够运行应用程序随意修改这个字典,当然这个字典中也包含了WSGI用到的其他数据,还有其他的一些系统特有的
扩展变量,命名约定之后讲解.

这个<tt class="docutils literal">start_response</tt>参数是一个callable的对象.
它接受2个位置参数,和一个可选的参数,为了演示方便,同样,命名为<tt class="docutils literal">status</tt>,
<tt class="docutils literal">response_headers</tt>, and <tt class="docutils literal">exc_info</tt>
,同样他们的命名不是只能这样,应用程序必须 **必须** 使用位置参数,如<tt class="docutils literal">start_response(status, response_headers)</tt>来触发着
callable的对象<tt class="docutils literal">start_response</tt>.

<tt class="docutils literal">status</tt>参数是一个表示状态的string,来源于<tt class="docutils literal">"999 Message here"</tt>
 ,还有<tt class="docutils literal">response_headers</tt>是一个由
<tt class="docutils literal">(header_name, header_value)</tt> tuples组成的http响应头.
可选参数<tt class="docutils literal">exc_info</tt>将在之后的章节
[The start_response() Callable](#the-start-response-callable) 和
[Error Handling](#error-handling)中讲到.
它被用作错误处理.例如返回浏览器一个错误信息.

当一个应用程序被server呼叫时,应用程序必须返回一个可以遍历的零个多个以上的字节流的对象,
这个可以有很多的实现方式,比如返回一个list,包含了很多的字节, 或者通过应用程序实现一个generator生成器
来返回多个字节流, 或者就是应用是一个类的实例,它是可以遍历的.考虑到怎么完成这个过程,
应用程序对象必须总是返回一个可以遍历生成多个字节string的.

server或者网关必须把生成的字节传送给客户端,不能是buffered的流,应该是一个完整的方式.
换句话说,应用程序应用程序 **必须** 完成他们字节的buffer,参见Buffering and
Streaming](#buffering-and-streaming) 节,

server和网关应该对待生成的字节string为二级制类的序列,而且,应该确保行结束符是没有被修改的.应用程序要负责
返回给客户端的字节string是一个正确的格式. server或者网关 **应该** 给http 传输加上编码,还有其他的一些传输
为了能够正确的实现其他的http特色.


如果一个请求是请求<tt class="docutils literal">len(iterable)</tt>的,而且成功了.server必须能够响应这个结果,
也就是说,如果一个可遍历的对象提供了一个可以工作的<tt class="docutils literal">__len__()</tt>的方法,他应该能够返回一个计算结果
详见[Handling the Content-Length Header](#handling-the-content-length-header)节,


如果应用程序返回的对象有一个<tt class="docutils literal">close()</tt>方法,
那么server或者网关就必须在当前请求结束的时候请求这个方法,或者在应用程序发生错误的时候请求他,
这个<tt class="docutils literal">close()</tt>方法需要支持通过应用程序发布资源,这个协议试图实现

应用程序返回一个生成器,或者自己实现的可遍历的对象,不应该假设他们会被完全使用,有可能提前就终止了.
注意:
应用程序必须触发 <tt class="docutils literal">start_response()</tt>这个可呼叫对象在真正取到响应内容之前.
注意可以先获得响应头部,然后再返回内容,尽管这个调用可能在遍历的第一次执行的时候被执行,server也不能够假设<tt class="docutils literal">start_response()</tt>
已经被调用了.


最后,server还有网关不能够直接使用iterable的其他属性,除非对于这个服务器来是一个特定的属性,例如file wrpper
返回一个<tt class="docutils literal">wsgi.file_wrapper</tt> (see [Optional
Platform-Specific File Handling](#optional-platform-specific-file-handling)).
一般来说,只有在这里提到的属性或者可以访问的,例如[PEP 234](/dev/peps/pep-0234)遍历api,是可以接受的.