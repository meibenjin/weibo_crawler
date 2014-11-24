weibo_crawler
=============

本工具使用模拟登录来实现微博搜索结果的爬取，如果用户需要爬取更多的数据，请在weibo\_zhanghao.txt中添加微博帐号的用户名密码（可以注册小号)，每一行一个账户，用户名和密码用逗号隔开。**希望更多的使用者能贡献注册的小号，这样能方便大家的爬取**

环境要求
----------------------
1. Python

    系统中需要先安装Python，这是Python官网链接[http://www.python.org](http://www.python.org)
    
2. BeautifulSoup

    BeautifulSoup是Python的一个html解析库，用来解析微博搜索结果中相关信息，版本是BeautifulSoup4, 安装方法可自行百度
    
    有关BeautifulSoup的更多信息，请访问[http://www.crummy.com/software/BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)

3. mysql-python
    
    访问mysql数据库的python模块，Ubuntu下安装方法见：[http://www.cnblogs.com/meibenjin/archive/2012/12/04/2801699.html](http://www.cnblogs.com/meibenjin/archive/2012/12/04/2801699.html)


使用
-----------------------
将要查询的关键词添加到keywords文件中，并启动程序

        python ./Crawler.py
工具提供两种保存方法，保存文件或写入数据库，通过修改weibo.ini实现

    1. 数据库：将weibo.ini中的enable字段设置为True,并设置数据库连接信息。表结构分别在WeiboContent.py和UserInfo.py的开头
    2. 文件：设置enable字段为False，则默认写入文件，分别为user\_info和weibo\_info

关于爬取时间间隔
----------------------
微博爬取中，如果爬取过快，会导致帐号被封，需要输入验证码，因此，工具里面每爬取一页会有一定时间休眠，在类SinaSearchCrawler的randomSleep和randomSnap中，每爬取一页，randomSnap一次，如果出现帐号被封，则会randomSleep，时间较长，唤醒后会切换帐号重新爬取
每个页面默认重试3次

注意
----------------------

该工具是在Linux下开发，所有文件以及程序都采用UTF-8编码，如果要在其他环境下运行，请注意修改相应的编码，强烈建议在Linux环境下运行



