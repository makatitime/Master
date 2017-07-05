#!/usr/bin/env python
#--*-- coding:utf-8 --*--
import urllib
import urllib2
url = 'http://bbs.meadin.com/thread-365344280-1-1.html'
user_agent = 'Mozilla/5.0 (NT 5.1; zh-CN; rv:1.8.0.11) Gecko/20070312 Firefox/1.5.0.11; 360Spider'
header = { 'User-Agent' : user_agent }
request = urllib2.Request(url, headers=header)
response = urllib2.urlopen(request)
pageCode = response.read().decode('utf-8')
print pageCode



