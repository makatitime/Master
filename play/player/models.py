# -*- coding:UTF-8 -*-
from django.db import models
# Create your models here.

'''
http://www.mobile-open.com/2016/105967.html
https://www.gitbook.com/book/wizardforcel/django-design-patterns-and-best-practices/details
http://www.jianshu.com/p/22d55fe44bdc
本地模型用到的字段类型和和参数的含义
max_length：最大长度
blank：True可以为空
null：可以为null
verbose_name：admin显示名称
default：默认值
unique：True表示唯一
【ImageField】：upload_to表示MEDIA_ROOT的子目录，用来存放上传的文件
【CharField】
【URLField】
【IntegerField】
【DateTimeField】：auto_now_add表示自动设置当前时间
【TextField】
【BooleanField】
【EmailField】
'''



class  articles(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=32)
    title = models.CharField(max_length=100)
    email = models.CharField(max_length=50,null=True)
    content = models.CharField(max_length=256)

    def __unicode__(self):
        return self.author

class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()
