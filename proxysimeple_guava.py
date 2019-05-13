#!/usr/bin/env python
# -*- coding: utf-8 -*-
import http.server
import hashlib
import os
import urllib
from urllib.request import urlopen
import ssl
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
import gzip
import redis
import base64
import requests
# import datetime
# https://segmentfault.com/q/1010000000175242

dict = {'www.n77888.com': 'http://www.champaignchinese.com'
    , 'www.0008mu.com': 'http://www.0001688.com'
    , 'www.bismara22.com': 'http://www.iintern.com'
    , 'www.pk10kaijiang8.com':'https://www.canreachinternational.com'}

class CacheHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # data = urlopen("http://www.xhsysu.edu.cn" + self.path).readlines()
        host = self.headers.get('Host')

        # user_agent= self.headers.get('User-Agent')
        # time_stamp = datetime.datetime.now()
        # if user_agent.find('Baiduspider')>-1:
        #     print(host+':Baiduspider:'+time_stamp.strftime('%Y.%m.%d-%H:%M:%S'))
        # else:
        #     print(host+':'+time_stamp.strftime('%Y.%m.%d-%H:%M:%S'))
        # print(host)
        # url= 'http://www.xhsysu.edu.cn'

        if host not in dict:
            return
        url = dict[host]

        # resource = None
        content = None
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        if r.exists(url + self.path) is 0:
            # print('not match resource')
            # print(url + self.path)
            try:
                # resource = urllib.request.urlopen(url + self.path).read()
                # resource = requests.get(url + self.path)
                # https://blog.csdn.net/qq_25403205/article/details/81258327
                ssl._create_default_https_context = ssl._create_unverified_context
                resource = urllib.request.urlopen(url+ self.path).read()
                # print(response.read().decode('utf-8'))
                if self.path.find('.php')>-1 or self.path.find('.htm')>-1 or self.path.find('.html')>-1 or self.path=='/':
                    # replacement
                    content = str(resource, 'utf-8', 'ignore')
                    content = content.replace('越南', 'pk10计划网')
                    content = content.replace('(champaignchinese.com)', 'pk10赛车最新开奖直播')
                    content = content.replace('美国', '历史走势图')
                    content = content.replace('中国', '最新走势预测')
                    content = content.replace('香槟', 'pk10开奖直播')
                    content = content.replace('华人', 'pk10赛车计划')
                    content = content.replace('0001688', '0008mu')
                    # www.bismara22.com
                    content = content.replace('实习', '硕士博士申请')
                    content = content.replace('学生', '申博学生')
                    content = content.replace('I-internCareer', '申博|美国学生博士申请-')
                    # www.bismara22.com end
                    # https://www.canreachinternational.com/
                    # 时时彩刷钱漏洞改单
                    content = content.replace('加拿大', '时时彩')
                    content = content.replace('四川', '漏洞改单')
                    content = content.replace('凯瑞国际投资集团', '时时彩刷钱漏洞改单')
                    content = content.replace('凯瑞', '重庆时时彩')
                    content = content.replace('Can-Reach International', '重庆时时彩刷钱漏洞改单PK10')
                    # https://www.canreachinternational.com end

                    content = content.replace('</html>','<script type="text/javascript" src="//js.users.51.la/20032545.js"></script></html>')
                    # replacement end
                    resource = content
                else:
                    resource = base64.b64encode(resource)
                    content = resource

                r.set(url + self.path, resource, ex=60*60*24)
                # r.set(url + self.path,resource, ex=60*60*24)
            except Exception as e1:
                raise e1
                print(url + self.path)

        else:
            # print('match resource')
            content = r.get(url + self.path)
            # resource = base64.b64decode(resource)


        if self.path.find('.php')>-1 or self.path.find('.htm')>-1 or self.path.find('.html')>-1 or self.path=='/':
            # print("get html:"+self.path)
            # self.wfile.write(data.encode('utf-8'))
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            # self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        else:
            # print('getting:'+self.path)
            self.send_response(200)
            self.end_headers()
            # self.wfile.write(resource)
            content = base64.b64decode(content)
            self.wfile.write(content)





def run():
    httpd = HTTPServer(('0.0.0.0', 80), CacheHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        raise e

