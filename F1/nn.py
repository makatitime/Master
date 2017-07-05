#!/usr/bin/env python
from collections import namedtuple

Friend = namedtuple("Friend", ['name', 'age', 'email'])

f1 = Friend('xiaowang', 33, 'xiaowang@163.com')
print(f1)
print(f1.age)
print(f1.email)
f2 = Friend(name='xiaozhang', email='xiaozhang@sina.com', age=30)
print(f2)

name, age, email = f2
print(name, age, email)


Friend(name='xiaowang', age=33, email='xiaowang@163.com')
33
xiaowang@163.com
Friend(name='xiaozhang', age=30, email='xiaozhang@sina.com')
('xiaozhang', 30, 'xiaozhang@sina.com')

person = namedtuple(names,ages,work)
f3 = person(wudi,11,hehe)
print f3

