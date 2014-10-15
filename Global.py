#!/usr/bin/python  
#-*- coding: utf-8 -*-
#
# Create by Meibenjin. 
#
# Last updated: 2014-04-11
#
# Global variables 

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
        line = fp.readline()
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


class LoginInfo:

    username = config.get('login', 'username')
    passwd = config.get('login', 'pswd')

    @staticmethod
    def printIt(prefix = ''):
        print 'Login Info:'
        print prefix, 'user:', LoginInfo.username
        print prefix, 'passwd:', LoginInfo.passwd

class CrawlerInfo:

    ids_path = config.get('crawl', 'idsDir')
    out_path = config.get('crawl', 'outPath')
    threads_num = config.getint('run', 'threadsNum')
    is_proxy = config.get('run', 'isProxy')

    @staticmethod
    def printIt(prefix = ''):
        print 'cralwer info:'
        print prefix, 'ids_path:', CrawlerInfo.ids_path
        print prefix, 'out_path:', CrawlerInfo.out_path
        print prefix, 'threads_num:', CrawlerInfo.threads_num
        print prefix, 'is_proxy:', CrawlerInfo.is_proxy


def test():
    LoginInfo.printIt('\t')
    CrawlerInfo.printIt('\t')

if __name__ == '__main__':
    test()
