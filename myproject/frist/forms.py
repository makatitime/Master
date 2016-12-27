from django import forms

class InfoForms(forms.Form):

    UserName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),label='UserName',max_length=16)
    PassWord = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),max_length=32)
    CHOICES = (('1', 'Man',), ('2', 'Female',))
    Gender = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
