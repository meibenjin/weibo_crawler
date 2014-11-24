#!/usr/bin/python  
#-*- coding: utf-8 -*-
#
# Create by Meibenjin. 
#
# Last updated: 2014-04-11
#
# Global variables 

import sys
reload(sys)
# if(sys.platform == 'win32'):
#     encoding = "gb2312"
# else:
#     encoding = "utf8"
    
sys.setdefaultencoding("utf8")

import random
import ConfigParser

CONFIG_PATH = './weibo.ini'

# read config file
config = ConfigParser.ConfigParser()
config.read(CONFIG_PATH)

def load_user_agent():
    user_agents = list()
    fp = open('./user_agents', 'r')

    line  = fp.readline().strip()
    while(line):
        user_agents.append(line)
        line = fp.readline().strip()
    fp.close()
    return user_agents

class UserAgents:
    
    user_agents = load_user_agent()
    
    @staticmethod
    def get_random_user_agent():
        length = len(UserAgents.user_agents)
        index = random.randint(0, length-1)
        user_agent = UserAgents.user_agents[index].strip()
        return user_agent

class DBInfo:
    
    host = config.get('Database', 'host')
    db = config.get('Database', 'db')
    user = config.get('Database', 'user')
    passwd = config.get('Database', 'passwd')
    port = config.getint('Database', 'port')
    enable = config.getboolean('Database', 'enable')
    
    @staticmethod
    def printIt(prefix = ''):
        print 'Database Info:'
        print prefix, 'host:', DBInfo.host
        print prefix, 'db:', DBInfo.db
        print prefix, 'user:', DBInfo.user
        print prefix, 'passwd:', DBInfo.passwd
        print prefix, 'port:', DBInfo.port
        print prefix, 'enable', DBInfo.enable

def test():
    LoginInfo.printIt('\t')
    CrawlerInfo.printIt('\t')

if __name__ == '__main__':
    test()
