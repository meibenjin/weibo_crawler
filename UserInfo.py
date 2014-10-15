#!/usr/bin/env python
# -*- coding: utf-8 -*-

class UserInfo():
    def __init__(self):
        self.id = ''
        self.screen_name = ''
        self.gender = ''
        self.birthday = ''
        self.labels = ''
        self.edu_label = ''
        self.career_label = ''
        self.province = ''
        self.city = ''
        self.location = ''
        self.description = ''
        self.follower_count = 0
        self.friends_count = 0
        self.weibo_count = 0
        self.url = ''
        self.verify_type =''


    def printIt(self):
        print "用户信息:"
        print "ID:", self.id
        print "昵称:", self.screen_name
        print "认证类型:", self.verify_type
        print "性别:", self.gender
        print "标签:", self.labels
        print "教育信息:", self.edu_label
        print "职业信息:", self.career_label
        print "省份:", self.province
        print "城市:", self.city
        print "所在地:", self.location
        print "简介:", self.description
        print "粉丝:", self.follower_count
        print "关注:", self.friends_count
        print "微博:", self.weibo_count
        print "博客:", self.url

    def writeFile(self, filename):
        wfile = open(filename, 'a')
        try:
            wfile.write(self.id + str(chr(94)))
            wfile.write(self.screen_name + str(chr(94)))
            wfile.write(self.verify_type + str(chr(94)))
            wfile.write(self.gender + str(chr(94)))
            wfile.write(self.labels + str(chr(94)))
            wfile.write(self.edu_label + str(chr(94)))
            wfile.write(self.career_label + str(chr(94)))
            wfile.write(self.province + str(chr(94)))
            wfile.write(self.city + str(chr(94)))
            wfile.write(self.location + str(chr(94)))
            wfile.write(self.description + str(chr(94)))
            wfile.write(str(self.follower_count) + str(chr(94)))
            wfile.write(str(self.friends_count) + str(chr(94)))
            wfile.write(str(self.weibo_count) + str(chr(94)))
            wfile.write(self.url)
            wfile.write('\n')
        except IOError, e:
            print 'file error:', e
        finally:
            wfile.close()
        

