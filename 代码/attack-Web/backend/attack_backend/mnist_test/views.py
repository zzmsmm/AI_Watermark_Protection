from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core import serializers
import json
from django.shortcuts import HttpResponse
import time
import itertools
from random import choice
import os
from numpy import number

import torch
from torch import nn
from torchvision import transforms
from PIL import Image

class CNN(nn.Module):
    def __init__(self):
        super(CNN,self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(1,16,3,1,1),  #16,28,28
            nn.ReLU(),
            nn.AvgPool2d(2,2)  #16,14,14
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(16,32,3,1,1),  #32,14,14
            nn.ReLU(),
            nn.AvgPool2d(2,2)  #32,7,7
        )
        self.conv3 = nn.Sequential(
            nn.Conv2d(32,64,2,1,1),  #64,8,8
            nn.ReLU(),
        )
        self.fc = nn.Sequential(
            nn.Linear(64*8*8,128),
            nn.ReLU(),
            nn.Linear(128,10)
        )
    def forward(self,x):
        x = x.to("cpu")
        x = x.reshape(-1,1,28,28)
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = x.view(x.size(0),-1)
        x = self.fc(x)
        return x

user_state = "Bob"

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
    file = open('mnist_test\circuit' + id + '.zip', 'rb') #文件名必须为英文，中文暂时无法正确解码
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream' #设置头信息，告诉浏览器这是个文件
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format('circuit' + id + '.zip')
    file.close()
    return response


@require_http_methods(["GET"])
def Download1(request):
    file = open('mnist_test\mykey.bk.pub', 'rb') #文件名必须为英文，中文暂时无法正确解码
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream' #设置头信息，告诉浏览器这是个文件
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format('mykey.bk.pub')
    file.close()
    return response


@require_http_methods(["POST"])
def Upload(request):
    files = request.FILES.getlist("file", None) # 接收前端传递过来的多个文件
    for file in files:
        print(os.getcwd())
        sql_path = f"{os.getcwd()}/mnist_test/upload/{file.name}"
        with open(sql_path, 'wb') as f:
            for content in file.chunks():
                # print(content)
                f.write(content)

    ## 插入model开始

    img = Image.open(sql_path).convert('L')
    img = img.resize((28, 28))
    img = transforms.ToTensor()(img)
    
    
    model = torch.load(os.getcwd() + "/mnist_test/cnn.pt", map_location='cpu')
    number = torch.argmax(model(img)).item()
    ## 插入model结束

    resp = {
        "code": 20000,
        "msg": 'success',
        "number": number,
        }
    return JsonResponse(resp)


@require_http_methods(["GET"])
def test(request): #test
    return