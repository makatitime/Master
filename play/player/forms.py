#--*-- coding:utf-8 --*--
from django import  forms

class ArtForms(forms.Form):
    your_name = forms.CharField(label='作者', max_length=100)
