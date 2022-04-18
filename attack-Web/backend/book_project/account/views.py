from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core import serializers
import json
from django.shortcuts import HttpResponse
import time
import itertools
from random import choice
import os

user_state = ''

@require_http_methods(["POST"])
def login(request):
    global  user_state
    body_json = request.body.decode()
    body_dict = json.loads(body_json)
    username = body_dict.get('username')
    password = body_dict.get('password')
    print(username, password)
    if (username == "Bob"):  # 用户登录
        user_state = '1'
        resp = {
            "code": 20000,
            "msg": 'successful'
        }
        return JsonResponse(resp)
    else:  # 企业登录
        user_state = '2'
        resp = {
            "code": 20000,
            "msg": 'successful'
        }
        return JsonResponse(resp)


@require_http_methods(["GET"])
def permission(request):
    resp = {
        "code": 20000,
        "msg": user_state
    }
    return JsonResponse(resp)


def logout(request):
    global user_state
    user_state = '0'
    resp = {
            "code": 20000,
            "data": "success"
        }
    return JsonResponse(resp)


@require_http_methods(["GET"])
def Download(request):
    print((request.GET.get("id")))
    id = request.GET.get("id")
    file = open('account\circuit' + id + '.zip', 'rb') #文件名必须为英文，中文暂时无法正确解码
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream' #设置头信息，告诉浏览器这是个文件
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format('circuit' + id + '.zip')
    file.close()
    return response


@require_http_methods(["GET"])
def Download1(request):
    file = open('account\mykey.bk.pub', 'rb') #文件名必须为英文，中文暂时无法正确解码
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream' #设置头信息，告诉浏览器这是个文件
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format('mykey.bk.pub')
    file.close()
    return response


@require_http_methods(["POST"])
def Upload(request):
    files = request.FILES.getlist("file",None) # 接收前端传递过来的多个文件
    for file in files:
        print(os.getcwd())
        sql_path = f"{os.getcwd()}/account/{file.name}"
        with open(sql_path, 'wb') as f:
            for content in file.chunks():
                # print(content)
                f.write(content)
    number = 0
    resp = {
        "code": 20000,
        "msg": 'success',
        "number": number,
        }
    return JsonResponse(resp)


@require_http_methods(["GET"])
def test(request): #test
    return