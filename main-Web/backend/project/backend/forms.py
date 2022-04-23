from django import forms


# 接收用的表单

class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=128)
    password = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput)


class registerForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=128)
    password1 = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', max_length=256, widget=forms.PasswordInput)
