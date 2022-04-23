from django.shortcuts import render
from django.shortcuts import redirect
from . import models


# from . import forms

# Create your views here.
def login(request):
    # 要求login视图的属性命名位username和password，并且加一个alert-warning的class，将显示消息命名为message
    if request.method == "POST":
        # login_form = forms.UserForm(request.post)
        username = request.POST.get('username')
        password = request.POST.get('password')
        # if login_form.is_valid():
        #    username = login_form.cleaned_data.get('username')
        #    password = login_form.cleaned_data.get('password')

        if username.strip() and password:
            try:
                user = models.User.objects.get(user_name=username)
            except:
                return render(request, '', {'message': '用户名不存在'})  # 失败返回当前界面
            if user.password == password:
                return redirect('')  # 登录成功的界面
            else:
                return render(request, '', {'message': '密码错误'})
    return render(request, '')


def register(request):
    if request.method == 'POST':
        # register_form = forms.RegisterForm(request.POST)
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        # if register_form.is_valid():
        if username.strip() and password1 and password2:
            # username = register_form.cleaned_data.get('username')
            # password1 = register_form.cleaned_data.get('password1')
            # password2 = register_form.cleaned_data.get('password2')
            if password1 != password2:
                return render(request, '', {'message': '两次密码输入不一样'})
            else:
                same_nameuser = models.User.objects.filter(user_name=username)
                if same_nameuser:
                    return render(request, '', {'message': '用户名已存在'})
            new_user = models.User()
            new_user.name = username
            new_user.password = password1
            return redirect('')  # 这里要返回登陆界面
    # register_form = forms.RegisterForm()
    return render(request, '', )
