#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import socket
import cookielib
import base64
import re
import time
import random
import json
import rsa
import binascii
import gzip, StringIO
import types

from Global import UserAgents
from UserInfo import UserInfo
from WeiboContent import WeiboContent
from bs4 import BeautifulSoup

_cookie_ = 'SINAGLOBAL=6487225655000.657.1410190073853; myuid=1762674087; un=meibenjin@gmail.com; wvr=5; SUS=SID-1762674087-1411904258-XD-e1kfs-7cacf03ee7f44c8dcf6028ea4105392e; SUE=es%3D656e767211466e7953d3c66359b4c959%26ev%3Dv1%26es2%3D067caf3508a526128bc8aa354bfbfc28%26rs0%3DJjXjIq%252BzJaELFwY9zM3dFNmPnl%252F9Z%252FHPsDsReSoy%252BohJ07KSrL2fNybmrZNIntrYriwzrVDQ39cYGncMMXQJ1CRZBB3%252BHNGQjNjvo1Ig2BOWgpn8lc1eV%252BRl9Arf0XAkDuV6O%252FLzUp65skUFj56bVX5HFqjWgvG3P3gfuJ%252FX484%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1411904258%26et%3D1411990658%26d%3Dc909%26i%3D392e%26us%3D1%26vf%3D0%26vt%3D0%26ac%3D2%26st%3D0%26uid%3D1762674087%26name%3Dmeibenjin%2540gmail.com%26nick%3Dmeibenjin%26fmp%3D%26lcp%3D2013-08-29%252016%253A58%253A58; SUB=_2AkMje3w1a8NlrAJWnvoTy2_iZIpH-jyQo3DDAn7uJhIyGxh-7gctqSWb_ZSuv3pvQHNnbTRcied4TOlG9A..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF9sHsjPHms29U08p7QAPKu5JpX5KMt; ALF=1443440258; SSOLoginState=1411904258; _s_tentry=login.sina.com.cn; UOR=,,login.sina.com.cn; Apache=6629540976136.923.1411904263337; ULV=1411904263404:47:47:2:6629540976136.923.1411904263337:1411886301878; BAYEUX_BROWSER=380c-yfn4sq95iogki0mcvv1cb2k; JSESSIONID=1gcrtz3gpiwyu1d2nwnijja320'


#login code from:  http://www.douban.com/note/201767245/
parameters = {
    'entry': 'weibo',
    'callback': 'sinaSSOController.preloginCallBack',
    'su': 'TGVuZGZhdGluZyU0MHNpbmEuY29t',
    'rsakt': 'mod',
    'checkpin': '1',
    'client': 'ssologin.js(v1.4.5)',
    '_': '1362560902427'
}

postdata = {
    'entry': 'weibo',
    'gateway': '1',
    'from': '',
    'savestate': '7',
    'useticket': '1',
    'pagerefer': '',
    'vsnf': '1',
    'su': '',
    'service': 'miniblog',
    'servertime': '',
    'nonce': '',
    'pwencode': 'rsa2',
    'rsakv': '',
    'sp': '',
    'encoding': 'UTF-8',
    'prelt': '27',
    'url': 'http://www.weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
    'returntype': 'META'
}

# 然后，urllib2的操作相关cookie会存在
# 所以登陆成功之后，urllib2的操作会带有cookie信息，抓网页不会跳转到登陆页
PROXY = 'http://10.77.30.62:808' 
proxy = urllib2.ProxyHandler({'http': PROXY}) 
cookiejar = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cookiejar)
#opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler, proxy)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)

class SinaLogin():
    
    
    def __init__(self):
        # 用户帐户列表，用于模拟登录
        self.username = list()
        self.passwd = list()
        self.read_account_list()
    
    def read_account_list(self):
        with open('weibo_zhanghao.txt') as weibo_file:
            for line in weibo_file:
                items = line.split(',')
                self.username.append(items[0].strip())
                self.passwd.append(items[1].strip())
                    
    def set_request(self, url, data, headers):
        self.request = urllib2.Request(
            url=url,
            data=data,
            headers=headers
        )
 
    def encrypt_username(self, uname):
        username_ = urllib.quote(uname)
        encrypt_username = base64.encodestring(username_)[:-1]
        return encrypt_username

    def encrypt_pwd(self, pwd, servertime, nonce, pubkey):
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, 65537) #创建公钥
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(pwd) #拼接明文 js加密文件中得到
        passwd = rsa.encrypt(message, key) #加密
        passwd = binascii.b2a_hex(passwd)  #将加密信息转换为16进制
        return passwd

    def get_server_time(self):
        url = 'http://login.sina.com.cn/sso/prelogin.php?' + urllib.urlencode(parameters)
        data = urllib2.urlopen(url).read()
        p = re.compile('\((.*)\)')
        try:
            json_data = p.search(data).group(1)
            data = json.loads(json_data)
            servertime = str(data['servertime'])
            nonce = data['nonce']
            pubkey = data['pubkey']
            rsakv = data['rsakv']
            return servertime, nonce, pubkey, rsakv
        except:
            print 'Get severtime error!'
            return None
        
    def login(self):
        if(len(self.username) < 1):
            print "微博用户不存在"
            return False
        index = random.randint(0, len(self.username) - 1)
        uname = self.username[index]
        pwd = self.passwd[index]
        
        url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.5)'
        try:
            servertime, nonce, pubkey, rsakv = self.get_server_time()
        except:
            return False

        global postdata
        postdata['servertime'] = servertime
        postdata['nonce'] = nonce
        postdata['rsakv'] = rsakv
        postdata['su'] = self.encrypt_username(uname)
        postdata['sp'] = self.encrypt_pwd(pwd, servertime, nonce, pubkey)
        postdata_encode = urllib.urlencode(postdata)
        
        user_agent = UserAgents.get_random_user_agent()

        headers = {
                'User-Agent': user_agent, 
                'Accept-Encoding':'gzip',
                'referer': 'http://www.weibo.com'
                }

        self.set_request(url, postdata_encode, headers)

        response = urllib2.urlopen(self.request)
        html = response.read()
        if(response.headers.get('content-encoding', None) == 'gzip'):
            html = gzip.GzipFile(fileobj=StringIO.StringIO(html)).read()

        p = re.compile('location\.replace\(.(.*?).\)')
        try:
            #如果没有异常返回，说明此时已自动登录，之后只需设置url和data就可以post或者直接get，
            #注意不要在request中设置header，这是因为cookie也是header的一部分，如果设置header会导致没有cookie，也就没有登录       
            login_url = p.search(html).group(1)
            urllib2.urlopen(login_url)
            return True
        except Exception , e:
            with open("./error_log", "a+") as test_file:
                test_file.write(html)
            print e
            return False

'''
微博爬取公共类
'''
class SinaSearchCrawler():
    base_url = "http://s.weibo.com"
    sina_user = None
    
    """
        模拟登录
    """
    def login(self):
        status = self.sina_user.login();
        if(status == True):
            print '登录成功.'
        else:
            print '登录失败.'
    
    def __init__(self):
        # 模拟一个用户并登录
        self.sina_user = SinaLogin()
        self.login()
        
        self.request = None
        timeout = 40
        socket.setdefaulttimeout(timeout)
    
    """
        随机分配睡眠时间
    Input:
        factor: 睡眠因子，因子越大，睡眠的时间越久
    """
    def randomSleep(self, factor):
        sleeptime =  random.randint(5, 10)
        time.sleep(sleeptime * factor)
        
    
    def randomSnap(self):
        sleeptime = random.randint(3, 5)
        time.sleep(sleeptime)
        #pass
    
    """
        根据URL获取网页源代码
    Input:
        url:网址
    Output:
        html:网页源代码
    """
    def get_html(self, url):
        html = None 
        retry = 3
        while(retry > 0):
            try:
                self.request = urllib2.Request(url=url);
                response = urllib2.urlopen(url)
                html = response.read()

                if(response.headers.get('content-encoding', None) == 'gzip'):
                    html = gzip.GzipFile(fileobj=StringIO.StringIO(html)).read()
                break;
            except urllib2.URLError,e:
                print 'url error:', e
                self.randomSleep(4 - retry)
                retry = retry - 1
                continue
            except Exception, e:
                print 'error:', e
                self.randomSleep(4 - retry)
                retry = retry - 1
                continue
        return html


'''
微博用户爬取类
'''
class UserSearchCrawler(SinaSearchCrawler):
    
    def __init__(self):
        SinaSearchCrawler.__init__(self)
        self.base_url = "%s/user" % SinaSearchCrawler.base_url
        
    """
        从网页中抽取微博用户信息
    Input:
        html: 搜索结果网页
    Output:
        user_info_list: 用户信息列表
                返回None表示爬取异常
    """
    def extract_user_info(self, html):
        user_info_list = list()
        # get json
        reg = re.compile(r'<script>STK && STK\.pageletM && STK\.pageletM\.view\((\{"pid":"pl_user_feedList".+?)\)</script>', re.I)
        match = reg.search(html)
        if(match):
            m = match.group(1)
            header_json = json.loads(m)
            if(type(header_json) == types.DictType):
                soup = BeautifulSoup(header_json['html'])

                # 获取微博用户列表
                user_list = soup.find_all("div", class_="person_detail")
                if(type(user_list) == types.NoneType):
                    return None
                for user in user_list:
                    user_info = UserInfo()
                    
                    # 获取用户的微博名称、ID、和博客地址
                    # 获取微博用户认证类型
                    p = user.find("p", class_="person_name")
                    
                    if(type(p) != types.NoneType):
                        links = p.find_all("a");
                        if(len(links) >= 1):
                            if(type(links[0]) != types.NoneType):
                                user_info.screen_name = links[0]["title"]
                                user_info.url = links[0]["href"]
                                user_info.id = links[0]["uid"]
                        
                        if(len(links) == 2):
                            if(type(links[1]) != types.NoneType):
                                img = links[1].find("img")
                                if(type(img) != types.NoneType):
                                    user_info.verify_type = img["title"]
                                
                    
                    #获取微博用户性别、地区
                    p = user.find("p", class_="person_addr")
                    if(type(p) != types.NoneType):
                        spans = p.find_all("span")
                        if(len(spans) >= 1):
                            if(type(spans[0]) != types.NoneType):
                                if(type(spans[0]["title"]) != types.NoneType):
                                    user_info.gender = spans[0]["title"]
                            user_info.location = ""
                        if(len(spans) == 2):
                            if(type(spans[1]) != types.NoneType):
                                user_info.location = spans[1].get_text().strip()
                                ars = user_info.location.split("，")
                                if(len(ars) == 1):
                                    user_info.province = ars[0]
                                    user_info.city = ""
                                if(len(ars) == 2):
                                    user_info.province = ars[0]
                                    user_info.city = ars[1]
                    
                    # 获取微博用户关注数、粉丝数和微博数
                    p = user.find("p", class_="person_num")
                    if(type(p) != types.NoneType):
                        spans = p.find_all("span")
                        if(len(spans) == 3):
                            link = spans[0].find("a")
                            if(type(link) != types.NoneType):
                                user_info.friends_count = link.get_text().strip()
                                link = spans[1].find("a")
                                user_info.follower_count = link.get_text().strip()
                                link = spans[2].find("a")
                                user_info.weibo_count = link.get_text().strip()
                    
                    # 获取微博用户简介
                    div = user.find("div", class_="person_info")
                    if(type(div) != types.NoneType):
                        p = div.find("p")
                        if(type(p) != types.NoneType):
                            user_info.description = p.get_text()[4:].strip();
                    
                    # 获取用户标签、教育信息、职业信息
                    ps = user.find_all("p", class_="person_label")
                    for p in ps:
                        if(p.get_text().find("标签") >= 0):
                            links= p.find_all("a")
                            for i in range(0, len(links)):
                                label = links[i].get_text().strip()
                                user_info.labels += label
                                if(i < len(links) -1):
                                    user_info.labels += ","
                        if(p.get_text().find("教育信息") >= 0):
                            link = p.find("a")
                            if(type(link) != types.NoneType):
                                user_info.edu_label = link.get_text().strip()
                        if(p.get_text().find("职业信息") >= 0):
                            link = p.find("a")
                            if(type(link) != types.NoneType):
                                user_info.career_label = link.get_text().strip()
                    user_info_list.append(user_info)
        else:
            print "extract_user_info:get error"
        return user_info_list
    
    """
        根据爬取的第一页的结果分析结果总数，并计算需要爬取的页数，最大可爬取页数不超过50页
    Input:
        html:爬取的搜索结果第一页源代码
    Output:
        pages_num: 结果页数
    """
    def get_pages(self, html):
        # get json
        reg = re.compile(r'<script>STK && STK\.pageletM && STK\.pageletM\.view\((\{"pid":"pl_user_feedList".+?)\)</script>', re.I)
        match = reg.findall(html)
        res = None
        if(match):
            for m in match:
                header_json = json.loads(m)
                if(type(header_json) == types.DictType):
                    soup = BeautifulSoup(header_json['html'])

                    # 获取微博搜索结果数
                    div = soup.find("div", class_="search_num")
                    if(type(div) != types.NoneType):
                        span = div.find("span")
                        if(type(span) != types.NoneType):
                            patten = re.compile(r'(\d+)')
                            match = patten.search(span.get_text())
                            if(match != None):
                                res = match.group(0).strip()
    
        if(res == None):
            return 0
        
        results_num = int(res)
        pages_num = 0
        # 每页显示的结果为20个，以下用来计算页数
        if(results_num % 20 == 0):
            pages_num =  results_num / 20
        else:
            pages_num =  results_num / 20 + 1
        
        #如果计算出的页数超过50页，返回最大页数50
        if(pages_num > 50):
            pages_num = 50
        
        return pages_num
                            
                    
    """
        通过关键词搜索微博用户信息
    Input:
        keyword: 搜索关键词，默认为新三板
        page: 搜索结果的页数，默认为所有页
    Output:
        user_list: 用户信息列表
    """
    def search(self, keyword="新三板", pages=0):
        user_list = list()
        
        # 获取搜索结果页数
        retry = 3
        while(retry > 0):
            req_url = "%s/%s" % (self.base_url, keyword)
            #获取第一页搜索结果
            html =  self.get_html(req_url)
            # 首先判断搜索结果页数是否为0，0表示默认爬取所有页
            if(pages == 0):
                # 根据第一页结果得到搜索结果页数
                pages = self.get_pages(html)
                if(pages == 0):
                    print "爬取异常，等待。。。"
                    self.randomSleep(4 - retry)
                    print "等待结束，切换登录用户重新开始尝试"
                    self.login()
                    retry = retry - 1
                else:
                    retry = 0
        
        # 分页获取搜索结果
        for i in range(1, pages + 1):
            #每个页面尝试3次
            retry = 3
            req_url = "%s/%s&page=%d" % (self.base_url, keyword, i)
            while(retry > 0):
                print "开始爬取第 %d 页" % i
                #第一页不用再次爬取
                if(i != 1):
                    html =  self.get_html(req_url)
                    
                user_infos = self.extract_user_info(html)
                if(type(user_infos) != types.NoneType):
                    if(len(user_infos) > 0):
                        for user_info in user_infos:
                            user_info.writeFile("./user_info")
                        user_list.extend(user_infos)
                        retry = 0
                    else:
                        print "爬取异常，等待。。。"
                        self.randomSleep(4 - retry)
                        print "等待结束，切换登录用户重新开始尝试"
                        self.login()
                        retry = retry - 1
                else:
                    print "该页没有结果"
                    continue
                
                #每爬取完一页以后随机睡眠一段时间
                self.randomSnap()
        return user_list
    

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

'''
微博内容爬取类
'''
class WeiboSearchCrawler(SinaSearchCrawler):
    
    def __init__(self):
        SinaSearchCrawler.__init__(self)
        self.base_url = "%s/wb" % SinaSearchCrawler.base_url
    
    """
        从网页中抽取微博用户信息
    Input:
        html: 搜索结果网页
    Output:
        weibo_list: 用户信息列表
    """
    def extract_weibo(self, html):
        weibo_list = list()
        # get json
        reg = re.compile(r'<script>STK && STK\.pageletM && STK\.pageletM\.view\((\{"pid":"pl_wb_feedList".+?)\)</script>', re.I)
        match = reg.search(html)
        if(match):
            m = match.group(1)
            header_json = json.loads(m)
            if(type(header_json) == types.DictType):
                soup = BeautifulSoup(header_json['html'])
                
                #获取微博搜索结果主DIV
                div = soup.find("div", class_="feed_lists W_linka W_texta")
                if(type(div) == types.NoneType):
                    return weibo_list
                
                # 获取微博用户列表
                wb_list = div.find_all("dd", class_="content")
                if(type(wb_list) == types.NoneType):
                    return weibo_list
                
                for wb in wb_list:
                    weibo = WeiboContent()
                    
                    #获取微博的内容(所属用户, 微博内容)
                    p_weibo = wb.find("p", attrs={"node-type":"feed_list_content"})
                    if(type(p_weibo) != types.NoneType):
                        link = p_weibo.find("a")
                        if(type(link) != types.NoneType):
                            #用户微博昵称
                            weibo.screen_name = link["title"]
                            
                            #用户ID
                            idstr = link["usercard"]
                            id_pattern = re.compile(r'id=([0-9]+)')
                            id_m = id_pattern.search(idstr)
                            if(id_m):
                                weibo.id = id_m.group(1)
                        
                        #微博内容(注意要处理微博中的url)
                        content = p_weibo.find("em", class_=None)
                        if(type(content) != types.NoneType):
                            links = content.find_all("a")
                            for link in links:
                                link_str = link.get_text()
                                if(link_str.find("@") >= 0):
                                    weibo.content_at_url[link_str] = link['href']
                                else:
                                    weibo.content_url.append(link['href'])
                                    
                            weibo.content = content.get_text()
                    
                    #微博发布时间
                    p_time = wb.find("p", class_="info W_linkb W_textb")
                    if(type(p_time) != types.NoneType):
                        link = p_time.find("a", class_="date")
                        if(type(link) != types.NoneType):
                            weibo.time = link['title']
                            
                    weibo.printIt()
                    weibo_list.append(weibo)
                
        else:
            print "extract_weibo:get error"
        return weibo_list
        
    """
        根据爬取的第一页的结果分析结果总数，并计算需要爬取的页数，最大可爬取页数不超过50页
    Input:
        html:爬取的搜索结果第一页源代码
    Output:
        pages_num: 结果页数
    """
    def get_pages(self, html):
        # get json
        reg = re.compile(r'<script>STK && STK\.pageletM && STK\.pageletM\.view\((\{"pid":"pl_wb_feedList".+?)\)</script>', re.I)
        match = reg.findall(html)
        res = None
        if(match):
            for m in match:
                header_json = json.loads(m)
                if(type(header_json) == types.DictType):
                    soup = BeautifulSoup(header_json['html'])

                    # 获取微博搜索结果数
                    div = soup.find("div", class_="search_num")
                    if(type(div) != types.NoneType):
                        span = div.find("span")
                        if(type(span) != types.NoneType):
                            patten = re.compile(r'(\d+)')
                            match = patten.search(span.get_text())
                            if(match != None):
                                res = match.group(0).strip()
    
        if(res == None):
            return 0
        
        results_num = int(res)
        pages_num = 0
        # 每页显示的结果为18个，以下用来计算页数
        if(results_num % 18 == 0):
            pages_num =  results_num / 18
        else:
            pages_num =  results_num / 18 + 1
        
        #如果计算出的页数超过50页，返回最大页数50
        if(pages_num > 50):
            pages_num = 50
        
        return pages_num
    
    #普通搜索
    def search(self, keyword="新三板", pages = 0):
        weibo_list = list()
        
        #设置爬取失败重试次数
        retry = 3
        # 获取第一页搜索结果并计算搜索结果页数
        req_url = "%s/%s&xsort=time" % (self.base_url, keyword)
        while(retry > 0):
            #获取第一页搜索结果
            html =  self.get_html(req_url)
            # 首先判断搜索结果页数是否为0，0表示默认爬取所有页
            if(pages == 0):
                # 根据第一页结果得到搜索结果页数
                pages = self.get_pages(html)
                if(pages == 0):
                    print "爬取异常，等待。。。"
                    self.randomSleep(4 - retry)
                    print "等待结束，切换登录用户重新开始尝试"
                    self.login()
                    retry = retry - 1
                else:
                    retry = 0
        
        print pages
        # 分页获取搜索结果
        for i in range(1, pages + 1):
            #每个页面尝试3次
            retry = 3
            req_url = "%s/%s&xsort=time&page=%d" % (self.base_url, keyword, i)
            while(retry > 0):
                print "开始爬取第 %d 页" % i
                #第一页不用再次爬取
                if(i != 1):
                    html =  self.get_html(req_url)

                weibo_infos = self.extract_weibo(html)
                #写入相应的文件
                if(type(weibo_infos) != types.NoneType):
                    if(len(weibo_infos) > 0):
                        for weibo_info in weibo_infos:
                            weibo_info.writeFile("./weibo_info")
                        weibo_list.extend(weibo_infos)
                        retry = 0
                    else:
                        print "爬取异常，等待。。。"
                        self.randomSleep(4 - retry)
                        print "等待结束，切换登录用户重新开始尝试"
                        self.login()
                        retry = retry - 1
                else:
                    print "该页没有结果"
                    continue
                
                self.randomSnap()
                    
        return weibo_list
    
    #高级搜索(按照地区搜索)
    def gsearch(self, keword="新三板", province="北京", city="所有城区"):
        pass
        

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#


"""
该类使用Cookie实现登录
需要定时更换Cookie, 算是半自动化
"""
class SinaLogin_Cookie:
    def __init__(self):
        # fill with your weibo.com cookie
        #COOKIE = ''
        pass
    def login(self):
        headers = {"cookie": _cookie_}
        url = 'http://www.weibo.com'
        req = urllib2.Request(url, headers=headers)
        text = urllib2.urlopen(req).read()
    
        pat_title = re.compile('<title>(.+?)</title>')
        r = pat_title.search(text)
        if r:
            if r.group(1).find("微博") >= 0 :
                return True
            else:
                return False
        
