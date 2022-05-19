from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
import os
import json
import hashlib
import random
import time
from . import models

import zipfile

# backdoor need
from urllib import response
import requests
import os
from PIL import Image


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


# 先产生随机数，再取其md5为密钥
def generate_key():
    rand_num = random.randint(0, 2147483647)
    return hashlib.md5(str(rand_num).encode('utf-8')).hexdigest()


@require_http_methods(["POST"])
def certification_apply(request):
    body_json = request.body.decode()
    body_dict = json.loads(body_json)
    print(body_dict)
    token = body_dict['token']
    user = models.User.objects.get(token=token)
    new_request = models.RequestInfo()
    new_request.user_name = user.user_name
    new_request.watermark_type = body_dict['watermark_type']
    new_request.model_type = body_dict['model_type']
    new_request.key = generate_key()
    new_request.hash = hashlib.md5(new_request.key.encode('utf-8')).hexdigest()
    new_request.save()
    resp = {
            "code": 20000,
            "message": "success",
            "hash": new_request.hash
        }
    return JsonResponse(resp)


@require_http_methods(["GET"])
def certification_list(request):
    token = request.GET.get('token')

    # 先通过token获取用户名
    try:
        user = models.User.objects.get(token=token)
    except models.User.DoesNotExist:
        return JsonResponse({
            "code": 60204,
            "message": "User Not Found"
        })

    # 再通过用户名获取记录
    try:
        data = models.AuthenticationRecord.objects.filter(user_name=user.user_name)
    except models.AuthenticationRecord.DoesNotExist:
        return JsonResponse({
            "code": 60204,
            "message": "Record Not Found"
        })
    data = list(data.values())
    # print(data)
    for row in data:
        algorithm = models.RecommendAlgorithm.objects.filter(watermark_type=row['watermark_type'],
                                                             model_type=row['model_type'])
        algorithm = models.WaterMarkAlgorithm.objects.get(algorithm_name=algorithm[0].algorithm_name)
        row['algorithm_name'] = algorithm.algorithm_name
        row['algorithm_detail'] = algorithm.algorithm_detail
    # print(data)
    resp = {
        "code": 20000,
        "data": data
    }
    return JsonResponse(resp)


# 测试成功（多条数据返回如何处理，如何在json中添加新元素，推荐算法查询）
@require_http_methods(["GET"])
def unfinished_list(request):
    token = request.GET.get('token')
    # print(token)
    # 先通过token获取用户名
    try:
        user = models.User.objects.get(token=token)
    except models.User.DoesNotExist:
        return JsonResponse({
            "code": 60204,
            "message": "User Not Found"
        })
    # print(user)
    # 再通过用户名获取记录
    try:
        data = models.RequestInfo.objects.filter(user_name=user.user_name)
    except models.RequestInfo.DoesNotExist:
        return JsonResponse({
            "code": 60204,
            "message": "Record Not Found"
        })
    data = list(data.values())
    # print(data)
    for row in data:
        algorithm = models.RecommendAlgorithm.objects.filter(watermark_type=row['watermark_type'],
                                                             model_type=row['model_type'])
        row['algorithm_name'] = algorithm[0].algorithm_name
    # print(data)
    resp = {
        "code": 20000,
        "data": data
    }
    return JsonResponse(resp)


@require_http_methods(["GET"])
def unfinished_detail(request):
    hash = request.GET.get('hash')
    record = models.RequestInfo.objects.get(hash=hash)
    algorithm = models.RecommendAlgorithm.objects.filter(watermark_type=record.watermark_type,
                                                         model_type=record.model_type)
    algorithm = models.WaterMarkAlgorithm.objects.get(algorithm_name=algorithm[0].algorithm_name)
    resp = {
        "code": 20000,
        "data": {
            "watermark_type": record.watermark_type,
            "model_type": record.model_type,
            "algorithm_name": algorithm.algorithm_name,
            "key_generate": algorithm.key_generate,
            "algorithm_detail": algorithm.algorithm_detail,
            "authentication_data_type": algorithm.authentication_data_type,
        }
    }
    return JsonResponse(resp)


def un_zip(file_name, hash):
    zip_file = zipfile.ZipFile(file_name)
    '''
    if os.path.isdir(file_name.split('.')[0]):
        pass
    else:
        os.mkdir(file_name.split('.')[0])
    '''
    for names in zip_file.namelist():
        if hash != names.split('/')[0]:
            zip_file.close()
            os.remove(file_name)
            return False
        zip_file.extract(names, f"{os.getcwd()}/backend/certification_data")
    zip_file.close()
    os.remove(file_name)
    return True


@require_http_methods(["GET"])
def download_key(request):
    # print((request.GET.get("hash")))
    hash = request.GET.get("hash")
    record = models.RequestInfo.objects.get(hash=hash)
    algorithm = models.RecommendAlgorithm.objects.filter(watermark_type=record.watermark_type,
                                                         model_type=record.model_type)
    algorithm = models.WaterMarkAlgorithm.objects.get(algorithm_name=algorithm[0].algorithm_name)
    print(algorithm.key_generate)
    ''' TODO
    if algorithm.key_generate == 'common':
        ...  # return key
    else:
        ...  # return data
    '''
    key = record.key
    # print(key)
    key_path = f"{os.getcwd()}/backend/key/key.txt"
    with open(key_path, 'w') as f:
            f.write(key)
    file = open('backend\key\key.txt', 'rb')  # 文件名必须为英文，中文暂时无法正确解码
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(hash + '.key')
    file.close()
    return response


# 这个地方其实应该就是把RequestInfo里的数据转到AuthenticationData和AuthenticationRecord里
@require_http_methods(["GET"])
def finished_apply(request):
    hash = request.GET.get('hash')
    record = models.RequestInfo.objects.get(hash=hash)

    new_finished_record = models.AuthenticationRecord()
    new_finished_record.key = record.key
    new_finished_record.hash = record.hash
    new_finished_record.user_name = record.user_name
    new_finished_record.watermark_type = record.watermark_type
    new_finished_record.model_type = record.model_type
    # new_finished_record.timestamp = time.time()
    new_finished_record.save()
    record.delete()
    print(new_finished_record.timestamp)
    resp = {
        "code": 20000,
        "message": "success"
    }
    return JsonResponse(resp)


@require_http_methods(["POST"])
def certification_upload(request):
    # hash = request.get_full_path().split('%3D')[1]  # 从 POST url 中获取 hash 参数
    hash = request.POST.get('hash')
    record = models.RequestInfo.objects.get(hash=hash)
    algorithm = models.RecommendAlgorithm.objects.filter(watermark_type=record.watermark_type,
                                                         model_type=record.model_type)
    algorithm = models.WaterMarkAlgorithm.objects.get(algorithm_name=algorithm[0].algorithm_name)
    print(algorithm.authentication_data_type)

    files = request.FILES.getlist("file", None)  # 接收前端传递过来的多个文件
    for file in files:
        sql_path = f"{os.getcwd()}/backend/certification_data/{hash}.{file.name.split('.')[1]}"
        with open(sql_path, 'wb') as f:
            for content in file.chunks():
                f.write(content)
        ''' TODO
        对上传数据进行检查，符合规范保存
        '''
        if file.name.split('.')[1] == 'zip':
            print("unzip")
            if not un_zip(sql_path, hash):
                return JsonResponse({
                    "code": 60204,
                    "message": "数据文件命名不规范"
                })
        else:
            os.remove(sql_path)
            return JsonResponse({
                "code": 60204,
                "message": "压缩文件只接受zip格式"
            })
        try:
            new_finished_data = models.AuthenticationData.objects.get(hash=hash)
        except:
            new_finished_data = models.AuthenticationData()
        new_finished_data.hash = hash
        new_finished_data.authentication_data_path = sql_path.split('.')[0]  # 保存文件目录
        new_finished_data.save()

    resp = {
        "code": 20000,
        "message": 'success',
    }
    return JsonResponse(resp)


@require_http_methods(["POST"])
def judge_upload(request):
    hash = request.get_full_path().split('%3D')[1]  # 从 POST url 中获取 hash 参数
    print(hash)
    files = request.FILES.getlist("file", None)  # 接收前端传递过来的多个文件
    for file in files:
        print(os.getcwd())
        sql_path = f"{os.getcwd()}/backend/judge_data/{hash}.{file.name.split('.')[1]}"
        with open(sql_path, 'wb') as f:
            for content in file.chunks():
                # print(content)
                f.write(content)
        ''' TODO
            对上传数据进行检查，符合规范保存
        '''
        try:
            new_judge_data = models.JudgeData.objects.get(hash=hash)
        except:
            new_judge_data = models.JudgeData()
        new_judge_data.hash = hash
        new_judge_data.judge_data_path = sql_path
        new_judge_data.save()

    resp = {
        "code": 20000,
        "msg": 'success',
    }
    return JsonResponse(resp)


@require_http_methods(["POST"])
def judge_apply(request):
    body_json = request.body.decode()
    body_dict = json.loads(body_json)
    token = body_dict['token']
    user = models.User.objects.get(token=token)
    # print(token)
    hash = body_dict['hash']
    try:
        record = models.AuthenticationRecord.objects.get(hash=hash)
    except:
        return JsonResponse({
            "code": 60204,
            "message": "注册记录不存在"
        })
    if user.user_name != record.user_name:
        return JsonResponse({
            "code": 60204,
            "message": "您无权对该注册记录进行操作"
        })

    if record.watermark_type == '黑盒':
        url = body_dict['api']
        # url = "http://127.0.0.1:8001/upload/"
        data = models.AuthenticationData.objects.get(hash=hash)
        path1 = data.authentication_data_path
        lis = os.listdir(path1)
        try:
            for i in range(len(lis)):
                tar_file = {'file': (open(os.path.join(path1, lis[i]), 'rb'))}
                response = requests.post(url=url, files=tar_file)
                data = response.json()
                print(data['number'])
                # print(data)
        except:
            return JsonResponse({
                "code": 60204,
                "message": "API Not Found"
            })
    else:
        pass

    resp = {
        "code": 20000,
        "message": "success"
    }
    return JsonResponse(resp)