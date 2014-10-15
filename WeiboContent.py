#!/usr/bin/env python
# -*- coding: utf-8 -*-

class WeiboContent():
    def __init__(self):
        self.id = ''
        self.screen_name = ''
        self.verify_type = ''
        self.content = ''
        self.content_url = list()
        self.content_at_url = {}
        self.time = ''
        self.province = ''
        self.city = ''

    def printIt(self):
        print "用户信息:"
        print "ID:", self.id
        print "昵称:", self.screen_name
        print "认证类型:", self.verify_type
        print "微博内容:", self.content
        print "微博外链接:", self.content_url
        print "@好友：", self.content_at_url
        print "发布时间:", self.time
        print "省份:", self.province
        print "城市:", self.city

    def writeFile(self, filename):
        wfile = open(filename, 'a')
        try:
            wfile.write(self.id + str(chr(94)))
            wfile.write(self.screen_name + str(chr(94)))
            wfile.write(self.verify_type + str(chr(94)))
            wfile.write(self.content + str(chr(94)))
            wfile.write(self.time + str(chr(94)))
            wfile.write(self.province + str(chr(94)))
            wfile.write(self.city + str(chr(94)))
            wfile.write('\n')
        except IOError, e:
            print 'file error:', e
        finally:
            wfile.close()
        

