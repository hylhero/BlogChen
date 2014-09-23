###cheerfullchen的个人博客
网址: [d9chen.sinaapp.com/](http://d9chen.sinaapp.com/)

-------
#### 功能
1. 博客:[d9chen.sinaapp.com/blog/](http://d9chen.sinaapp.com/blog/)
2. 聊天室:[d9chen.sinaapp.com/chat/](http://d9chen.sinaapp.com/chat/)
3. 必应壁纸:[d9chen.sinaapp.com/photo/bing/](http://d9chen.sinaapp.com/photo/bing/)

####说明
* Python 版本 2.7.6
* Django 版本 1.6.5
* 使用了百度富文本编辑器[DjangoUeditor](https://github.com/zhangfisher/DjangoUeditor)
* 使用了[widget_tweaks](https://pypi.python.org/pypi/django-widget-tweaks),用于在模板中为form添加属性
* 使用了代码高亮插件[syntaxhighlighter](http://alexgorbatchev.com/SyntaxHighlighter/)
* 自己使用PIL库写了一个生成验证码的模块,但目前还未实现验证功能
* 使用了[Jquery](http://jquery.com/)
* 使用了[七牛Python SDK](http://developer.qiniu.com/docs/v6/sdk/python-sdk.html)
* 编程工具使用了[Sublime Text 2](http://www.sublimetext.com/)

####关于博客
* 目前实现了博文的列表展示,详情页面展示,评论列表展示,用户评论,关于界面
* 通过自己编写的标签,实现了在博文列表界面只展示整篇博文摘要信息
* 使用正则表达式,实现了博文摘要html标签补全功能
* 优化了模板,实现了在手机上也能达到良好显示的功能
* 目前博客不支持用户注册,订阅,邮件发送等功能,这些有待进一步开发