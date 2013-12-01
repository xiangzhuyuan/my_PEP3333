## 关于String类型

一般来说,http处理的是字节,也就是说这个定义文档基本上就是在说如何处理字节.
但是,通常都会有各种样的文本处理,在python当中,string就是非常方便的手段来处理文本.

但是在之前旧版本的Python实现中,对于string的实现有区别,string是unicode的,而非字节,这个
问题的存在就需要很小心的处理平衡http中可用api和正确的转换在字节和文本之间.特别是需要支持可移植的代码,
用不同的<tt class="docutils literal">str</tt>实现.

因此,WSGI实现了2种"string":

* "原生"字符串,它总是使用<tt class="docutils literal">str</tt>类来实现,用在处理request/response
和元数据上.
* "字节字符串",它是用<tt class="docutils literal">bytes</tt>类实现的,在python3当中,以及<tt class="docutils literal">str</tt>,
用来处理request/response的内容本身,e.g. POST/PUT输入数据和输出HTML.

不要被困扰:即使python的<tt class="docutils literal">str</tt>类用unicode实现,当前的string的_content_都会被转换为
字节通过Lating-1的编码.

之后的Unicode 问题中说明.

简而言之,在这个文章中看到的string,它指的是原生的string,例如一个<tt class="docutils literal">str</tt>的对象,
不管它的内部实现是unicde还是字节,当你看到它引用的是bytestring,他就是一个<tt class="docutils literal">bytes</tt>,
在python3中,在python2中他就是一个<tt class="docutils literal">str</tt>.

而且即使http处理的是字节,但是还是有很多的方便的方法来处理这些python中默认的<tt class="docutils literal">str</tt>类.