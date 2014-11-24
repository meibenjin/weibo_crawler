#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
# if(sys.platform == 'win32'):
#     encoding = "gb2312"
# else:
#     encoding = "utf8"
    
sys.setdefaultencoding("utf8")

try:
    
    import SinaAPI
except ImportError, e:
    print 'check module error:', e
    exit()

def read_keywords():
    keywords = list()
    fp = open("./keywords")
    line  = fp.readline().strip()
    while(line):
        keywords.append(line)
        line = fp.readline().strip()
    fp.close()

    return keywords;

def main():
    
    #if(len(sys.argv) < 2):
    #    print "python ./Crawler keyword user/weibo"
        
    #keyword = sys.argv[1].decode('gbk').encode("utf8")
    #search_type = sys.argv[2]
    #weibo_api = SinaAPI.WeiboSearchCrawler()
    #weibo_api.gsearch(keyword=keyword)
    
    keywords = read_keywords()
    for keyword in keywords:
        print "搜索关键词: %s" % keyword
        #搜索微博用户
        user_api = SinaAPI.UserSearchCrawler()
        user_api.search(keyword=keyword)
        #搜索微博
        weibo_api = SinaAPI.WeiboSearchCrawler()
        weibo_api.gsearch(keyword=keyword, pages=2)

if __name__ == '__main__':
    main()



