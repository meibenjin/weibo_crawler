#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
# if(sys.platform == 'win32'):
#     encoding = "gb2312"
# else:
#     encoding = "utf8"
    
sys.setdefaultencoding("utf8")
import time

from Global import DBInfo
from _mysql_exceptions import DatabaseError
from DBConnection import DBConnection

create_tbl = 'create table weibo_user(id varchar(20), screen_name varchar(50), gender varchar(4), verify_type varchar(20), labels varchar(200), edu_label varchar(50), career_label varchar(50), location varchar(20), province varchar(10), city varchar(10), description varchar(500), follower_count int, friends_count int, weibo_count int, url varchar(100), PRIMARY KEY (id))'

class UserInfo():
    def __init__(self):
        self.id = ''
        self.screen_name = ''
        self.gender = ''
        self.verify_type =''
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
    
    def insert_table(self):
        try:
            #sql = "insert into weibo_user values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%d,%d,%d,'%s')" % \
            #(self.id, self.screen_name, self.gender, self.verify_type, self.labels, self.edu_label, self.career_label, 
            #self.location, self.province, self.city, self.description, int(self.follower_count), 
            #int(self.friends_count), int(self.weibo_count), self.url)
             
            sql = "insert into weibo_user values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            
            query_sql = "select * from weibo_user where id = %s"
            
            delete_sql = "delete from weibo_user where id = %s"
            
            db = DBConnection()
        
            conn = db.get_conn()
            
            conn.select_db(DBInfo.db)
            cur = db.get_cursor()
            
            #首先检查数据库中是否已经存在, 如果存在则首先删除，然后插入新的微博用户
            count = cur.execute(query_sql, (self.id,))
            if(count != 0):
                cur.execute(delete_sql, (self.id,))
            
            ret = cur.execute(sql, (self.id, self.screen_name, self.gender, self.verify_type, \
                                  self.labels, self.edu_label, self.career_label, self.location, \
                                  self.province, self.city, self.description, self.follower_count, \
                                  self.friends_count, self.weibo_count, self.url))
            
            conn.commit()
            db.close()
            if(ret == 1):
                return True
            return False
        except DatabaseError, e:
            print "insert error", e
        
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
        

