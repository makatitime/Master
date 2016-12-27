#!/usr/bin/env python
#-*- coding:utf-8 -*-

__author__='Crkdoor'

class ComPany(object):
    def __init__(self,name,job):
        self.name = name
        self.job = job

    def tell(self):
        print '----Company is %s ---Job is %s' %(self.name,self.job)

s = ComPany('RCBC','Hacker')
s.tell()

