#--*-- coding:utf-8 --*--
from django import  forms
Gender_CHOICES = ('Man', 'Famel')
FAVORITE_COLORS_CHOICES = (
    ('blue', 'Blues'),
    ('green', 'Green'),
    ('black', 'Black'),
)

class ArtForms(forms.Form):
    name = forms.CharField(label='作者',required=True, max_length=100,error_messages={'required': '用户名不能为空', 'invalid': '名字不符合规范'})
    title = forms.CharField(label='标题',required=True, max_length=100,error_messages={'required': '标题不能为空', 'invalid': '标题包含非法字符'})
    pwd   = forms.CharField(label='密码',widget=forms.PasswordInput,required=True,error_messages={'required': '密码不能为空', 'invalid': '密码安全强度不够'})
    email = forms.EmailField(label='Email',required=True, max_length=50,error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'})
    content = forms.CharField(label='',widget=forms.Textarea,error_messages={'required': '内容不能为空', 'invalid': '内容包含非法字符'})
    img = forms.ImageField()
    favorite_colors = forms.MultipleChoiceField(required=False,
        widget=forms.CheckboxSelectMultiple, choices=FAVORITE_COLORS_CHOICES)
    gender = forms.ChoiceField(
        choices=((1, '男'), (2, '女'),),  # 定义下拉框的选项，元祖第一个值为option的value值，后面为html里面的值
        initial=1,  # 默认选中第二个option
        widget=forms.RadioSelect  # 插件表现形式为单选按钮
    )