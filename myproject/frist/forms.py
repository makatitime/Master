#coding:utf-8
from django import forms

class InfoForms(forms.Form):

    UserName = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'UserName'}),label='UserName:',max_length=16)
    PassWord = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'PassWord'}),label='PassWord:',max_length=32)
    Age = forms.IntegerField(required=True,widget=forms.PasswordInput({'class': 'form-control','placeholder':'Age'}),label='Age:')
    Email = forms.EmailField(label='邮箱:',required=True,widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Email'}))
    CHOICES = (('1', 'Man',), ('2', 'Female',))
    Gender = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
