from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
import os
import json
import hashlib
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
            "message": "用户不存在"
        })
    if user.password == password:
        token = user.token
        resp = {
            "code": 20000,
            "data": {
                "token": token
            }
        }
        return JsonResponse(resp)
    else:
        resp = {
            "code": 60204,
            "message": "密码错误"
        }
        return JsonResponse(resp)


@require_http_methods(["POST"])
def register(request):
    body_json = request.body.decode()
    body_dict = json.loads(body_json)
    username = body_dict.get('username')
    password = body_dict.get('password')
    email = body_dict.get('email')
    same_nameuser = models.User.objects.filter(user_name=username)
    if same_nameuser:
        resp = {
            "code": 20000,
            "message": "用户名已被使用"
        }
        return JsonResponse(resp)
    new_user = models.User()
    new_user.user_name = username
    new_user.password = password
    new_user.email = email
    new_user.token = hashlib.md5(username.encode("utf-8")).hexdigest()
    new_user.avatar = "default.png"
    new_user.save()
    resp = {
        "code": 20000,
        "message": "success"
    }
    return JsonResponse(resp)


@require_http_methods(["POST"])
def change_avatar(request):
    file = request.FILES.get('avatar_file')
    username = request.POST.get('avatar_name')
    user = models.User.objects.get(user_name=username)
    sql_path = f"{os.getcwd()}/media/avatar/{username}.png"
    with open(sql_path, 'wb') as f:
        for content in file.chunks():
            f.write(content)
    user.avatar = f"avatar/{username}.png"
    user.save()
    resp = {
        "code": 20000,
        "message": 'success',
        }
    return JsonResponse(resp)


@require_http_methods(["POST"])
def logout(request):
    resp = {
            "code": 20000,
            "message": "success"
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
    if user.user_name == "admin":
        role = 'admin'
    else:
        role = 'user'
    resp = {
        "code": 20000,
        "data": {
            "avatar": user.get_avatar_url(),
            "name": user.user_name,
            "email": user.email,
            "roles": [role],
        }
    }
    return JsonResponse(resp)