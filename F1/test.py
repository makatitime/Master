#!/usr/bin/env  python
# _*_ coding: utf-8 _*_

# name = raw_input("Please Input Your name:")
# age = raw_input("Please Input Your age:")
# hobby = raw_input("Please Input Your hobby :")
#
#
# print "My name is %s,%s years old, I like %s" %(name,age,hobby)
#
#
#

#       1. 判断，如果x不为负数和0，则输出 y
x = 858
y = 668

if x >0:
    print y


#2.如果 x >500, 并且 y <700，而输出“hahaha”，否则，输出 "hehehe"
if x > 500 and y <700:
    print "hahaha"
else:
    print "hehehe"
#二、a = 123 b = 234, 用两种方法进行判断，如果b大于a时，而输出 "b > a"
a = 123
b = 234

if b > a:
    print "b > a "
一、定义一个函数方法，名字为 test,可以接收任意多的整型参数，
    返回其中最大的和最小的值。


二、定义一个函数方法，名字为 test2,可以接收任意多的字符串，
    结果返回其中长度最长字符串。

def foo(*args, **kwargs):
    print 'args = ', args
    print 'kwargs = ', kwargs
    print '---------------------------------------'

if __name__ == '__main__':
    foo(1,2,3,4)
    foo(a=1,b=2,c=3)
    foo(1,2,3,4, a=1,b=2,c=3)
    foo('a', 1, None, a=1, b='2', c=3)

def test(*args):
    for i in args:
        print max(i)

l = [11,22,33,44,55,66]
test(l)

def test2(**kwargs):

1 定义一个方法get_num(n),n参数是列表类型，判断列表里面的元素是否为数字类型，其他类型则报错，最  终返回一个偶数列表：（注：列表里面的元素为偶数)



def get_num(n):

    for i in n:
        print i


n = [1,2,3,4,5]
get_num(n)


1 定义一个方法get_doc(func),func参数为任意一个函数对象，返回该函数对象的描述文档，
  如果该函数没有描述文档，则返回"Not found."


def get_doc(func):

    return func.__doc__


if get_doc == none:
    print 'Not Found'


get_doc('os')


2 定义一个方法get_sum(),求1-100范围内的所有数的平方和, 返回结果为整数类型。
  做好断言。

def get_sum(l):
    ss = 0
    for i in l:
        ss += i**2
    return ss

l = range(1,101)
assert isinstance(get_sum(l),int)


6.  首先查看 range(-10,10)返回的是什么？
     再用 filter 和 lambda 实现结果为 [6, 7, 8, 9]
l = range(-10,10)
lambda l :x for 
filter(funs,l)


类的名称为 student

1 姓名
2 年龄
3 成绩（语文，数学，英语)[每科成绩的类型为整数]

类方法：

1 获取学生的姓名：get_name() 要求返回类型为字符串。
2 获取学生的年龄：get_age() 要求返回类型为整型。
3 返回3门科目中最高的分数。get_max() 要求返回类型为整型。

写好类以后，可以定义2个同学测试下:

xm = student('xiaoming',20,[69,88,100])
返回结果：
xiaoming
20
100

dl = student('dalong',23,[82,60,99])

返回结果：
dalong
23
99

class student(object):
    def __init__(self,name,age,score):
        self.name = name
        self.age = age
        self.score = score
        self.get_name()
        self.get_age()
        self.get_socre()
    def get_name(self):
        print self.name
    def get_age(self):
        print self.age

    def get_socre(self,l):
        print l

dl = student('dalong',23,[82,60,99])
dl.get_name()

