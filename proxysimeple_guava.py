#!/usr/bin/env python
# -*- coding: utf-8 -*-
import http.server
import hashlib
import os
import urllib
from urllib.request import urlopen
from http.server import HTTPServer, BaseHTTPRequestHandler
import gzip

# https://segmentfault.com/q/1010000000175242


class CacheHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # data = urlopen("http://www.xhsysu.edu.cn" + self.path).readlines()
        url= 'http://www.xhsysu.edu.cn';
        resource = urllib.request.urlopen(url + self.path).read()
        content=''



        if self.path.find('.php')>-1 or self.path.find('.htm')>-1 or self.path.find('.html')>-1 or self.path=='/':
            print("get html:"+self.path)
            content = str(resource, 'utf-8', 'ignore')
            content = content.replace('中山大学', '大神学院')
            # self.wfile.write(data.encode('utf-8'))
            self.send_response(200)

            self.send_header("Content-type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        else:
            print('getting:'+self.path)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(resource)





def run():
    httpd = HTTPServer(('localhost', 8000), CacheHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    run()