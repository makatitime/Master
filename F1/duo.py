#!/usr/bin/env  python
#-*- coding:utf-8 -*-
import threading
import urllib
import urllib2
import re

urls = ['http://www.iplaypython.com', 'http://www.jd.com','http://www.taobao.com']

def gettitle(url):
    res = urllib2.Request(url)
    page = urllib2.urlopen(res)
    print page.getcode()
    content = page.read()
    pattern = re.compile(r'<title>(.*?)</title>', re.S)
    titles = re.findall(pattern,content)
    for title in titles:
            print title
for url in urls:
        t1 = threading.Thread(target=gettitle,args=(url,))
        t1.start()
