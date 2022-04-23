from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
import json
from . import models


# from . import forms

# Create your views here.
@require_http_methods(["POST"])
def login(request):
    body_json = request.body.decode()
    body_dict = json.loads(body_json)
    username = body_dict.get('username')
    password = body_dict.get('password')
    print(username, password)
    try:
        user = models.User.objects.get(user_name=username)
    except:
        return JsonResponse({
            "code": 60204,
            "message": "not_exist"
        })
    if user.password == password:
        token = user.token
        resp = {
            "code": 20000,
            "data" : {
                "token": token
            }
        }
        return JsonResponse(resp)
    else:
        resp = {
            "code": 60204,
            "message": "wrong_password"
        }
        return JsonResponse(resp)


@require_http_methods(["POST"])
def logout(request):
    resp = {
            "code": 20000,
            "data": "success"
        }
    return JsonResponse(resp)


@require_http_methods(["GET"])
def getinfo(request):
    token = request.GET.get("token")
    try:
        user = models.User.objects.get(token=token)
    except:
        return JsonResponse({
            "code": 60204,
            "message": "not_exist"
        })
    resp = {
        "code": 20000,
        "data": {
            "avatar": user.get_avatar_url(),
            "name": user.user_name
        }
    }
    return JsonResponse(resp)


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
