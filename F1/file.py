#!/usr/bin/env  python
# -*- coding:utf-8 -*-
__author__="Crkdoor"
# print "今天"
# name = "Makati台风"
# print(name)
# print len(name)
# name_list = [name,'TTTT']
# print(name_list)
# name1 = u"Makati台风"
# print len(name1)
# name_list1 = [name1,'TTTT']
# print(name_list1)
#
# products = [
# 	['apple',4000],
# 	['ipad',3000],
# 	['watch',2000],
# 	['clothes',1000],
# 	['shoes',800],
# 	['coffe',100],
# 	]
# salary = 10000
# shop_list = []
# while True:
# 	for index,p in enumerate(products):
# 		print index,p[0],p[1]
# 	choise = raw_input("Chose You want buy:").strip()
# 	if choise.isdigit():
# 		choise = int(choise)
# 		price = products[choise][1]
# 		if price < salary:
# 			shop_list.append(products[choise][0])
# 			salary -= price
# 			print "Your Shop List is %s Your Blance is %s " %(shop_list,salary)
# 		else:
# 			choise = 'quit'
#
# 	if choise == 'quit':
# 		print 'BYE BYE'
# 		break

print __author__

def ceshi(*args):
	print args

def ceshi1(**kwargs):
	print kwargs

ceshi(1,2,3)
print map(ceshi,range(22))
ceshi1(a=4,b=5,c=6)



