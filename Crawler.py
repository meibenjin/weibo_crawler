#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import sys
    import SinaAPI
except ImportError, e:
    print 'check module error:', e
    exit()

def main():
    
    if(len(sys.argv) < 2):
        print "python ./Crawler keyword user/weibo"
    keyword = sys.argv[1]
    search_type = sys.argv[2]
    
    if(cmp(search_type, "user") == 0):
        user_api = SinaAPI.UserSearchCrawler()
        user_api.search(keyword=keyword)
    else:
        weibo_api = SinaAPI.WeiboSearchCrawler()
        weibo_api.search(keyword=keyword)

if __name__ == '__main__':
    main()



