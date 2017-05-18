#--*-- coding:utf-8 --*--
from django import  forms

class ArtForms(forms.Form):
    name = forms.CharField(label='作者', max_length=100)
    title = forms.CharField(label='标题', max_length=100)
    content = forms.CharField(label='',widget=forms.Textarea)
