#coding:utf-8
from django import forms

class InfoForms(forms.Form):

    UserName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),label='UserName:',max_length=16,required=True)
    PassWord = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),label='PassWord:',max_length=32,required=True)
    CHOICES = (('1', 'Man',), ('2', 'Female',))
    Gender = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    Email = forms.EmailField(label='邮箱:',required=True,widget=forms.EmailInput(attrs={'class': 'form-control'}))