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


使用
-----------------------
1. 查询微博人物
        
        python ./Crawler "keyword" user
2. 查询微博内容
        
        python ./Crawler "keyword" weibo

注意!!!!
----------------------

该工具是在Linux下开发，所有文件以及程序都采用UTF-8编码，如果要在其他环境下运行，请注意修改相应的编码，强烈建议在Linux环境下运行



