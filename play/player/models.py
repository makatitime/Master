from django.db import models

# Create your models here.
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
