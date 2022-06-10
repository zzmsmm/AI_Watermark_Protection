from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.shortcuts import HttpResponse
import json
import hashlib
from . import models

# backdoor need
import requests
from PIL import Image

# whitebox need
import torch
import qrcode
from torch.utils.data import Dataset
import torch.utils.data as Data
import torchvision
import random
import numpy as np
import zipfile
import os
import shutil


class QRDataset(Dataset):
    def __init__(self, txt_path, sql_path, transform=None, target_transform=None):
        fh = open(txt_path, 'r')
        imgs = []
        for line in fh:
            line.rstrip()
            words= line.split()
            # imgs.append((sql_path + '/qrdataset/' + words[0], int(words[1])))
            imgs.append((sql_path + '/qrdataset/' + words[0].split('/')[2], int(words[1])))
        self.imgs = imgs
        self.transform = transform
        self.target_transform = target_transform

    def __getitem__(self, index):
        fn, label = self.imgs[index]
        img = Image.open(fn).convert('RGB')
        if self.transform is not None:
            img = self.transform(img)
        return img, label

    def __len__(self):
        return len(self.imgs)


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


def un_zip(file_name, hash, situation):
    zip_file = zipfile.ZipFile(file_name)
    for names in zip_file.namelist():
        if hash != names.split('/')[0]:
            zip_file.close()
            os.remove(file_name)
            return False
        if situation == 0:
            zip_file.extract(names, f"{os.getcwd()}/backend/certification_data")
        else:
            zip_file.extract(names, f"{os.getcwd()}/backend/judge_data")
    zip_file.close()
    os.remove(file_name)
    return True


def gen_qr(n, content, sql_path):
    if os.path.isdir(f"{sql_path}/qrdataset/"):
        pass
    else:
        os.mkdir(f"{sql_path}/qrdataset/")
    prefix = f"{sql_path}/qrdataset/"
    for i in range(n):
        qr = qrcode.QRCode(
            version=4,
            error_correction=qrcode.constants.ERROR_CORRECT_Q,
            box_size=3.5,
            border=0,
        )
        qr.add_data(content[i])
        img = qr.make_image()
        filename = prefix + str(i) + ".png"
        img.save(filename)


def gen_seed(value):
    int_value = int(("0x"+value), 16)
    return int_value % 2**32


@require_http_methods(["GET"])
def download_key(request):
    hash = request.GET.get("hash")
    record = models.RequestInfo.objects.get(hash=hash)
    algorithm = models.RecommendAlgorithm.objects.filter(watermark_type=record.watermark_type,
                                                         model_type=record.model_type)
    algorithm = models.WaterMarkAlgorithm.objects.get(algorithm_name=algorithm[0].algorithm_name)
    print(algorithm.key_generate)

    if algorithm.key_generate == 'common':
        key = record.key
        key_path = f"{os.getcwd()}/backend/key/key.txt"
        with open(key_path, 'w') as f:
            f.write(key)
        file = open('backend\key\key.txt', 'rb')  # 文件名必须为英文，中文暂时无法正确解码
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(hash + '.key')
        file.close()
        return response
    else:
        sql_path = f"{os.getcwd()}/backend/certification_data/{hash}"
        if os.path.isdir(sql_path):
            pass
        else:
            os.mkdir(sql_path)

        serial = record.key
        num = 10
        content = []
        for i in range(100):
            content.append(serial+'-'+('%04d' % i))
        gen_qr(num, content, sql_path)

        arr_1 = np.array(range(0, num, 1))
        np.random.seed(gen_seed(serial))
        np.random.shuffle(arr_1)
        arr_2 = [0] * int(num / 2) + [1] * int(num / 2)
        np.random.shuffle(arr_2)
        f = open(f"{sql_path}/index.txt", 'w')
        for i in range(0, num):
            f.write('./qrdataset/' + str(arr_1[i]) + '.png ' + str(arr_2[i]) + '\n')
        f.close()

        filenames = os.listdir(f"{sql_path}/qrdataset/")
        with zipfile.ZipFile('qrdataset.zip', "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(f"{sql_path}/index.txt", "index.txt")
            for item in filenames:
                zf.write(f"{sql_path}/qrdataset/" + item, "qrdataset/" + item)

        file = open('qrdataset.zip', 'rb')  # 文件名必须为英文，中文暂时无法正确解码
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(hash + '.zip')
        file.close()

        os.remove('qrdataset.zip')
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

        if file.name.split('.')[1] == 'zip':
            print("unzip")
            if not un_zip(sql_path, hash, 0):
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

        '''
        check data
        '''

    try:
        new_finished_data = models.AuthenticationData.objects.get(hash=hash)
    except:
        new_finished_data = models.AuthenticationData()
    new_finished_data.hash = hash
    new_finished_data.authentication_data_path = sql_path.split('.')[0]
    new_finished_data.save()

    resp = {
        "code": 20000,
        "message": 'success',
    }
    return JsonResponse(resp)


@require_http_methods(["POST"])
def judge_upload(request):
    hash = request.POST.get('hash')
    print(hash)
    try:
        record = models.AuthenticationRecord.objects.get(hash=hash)
    except:
        return JsonResponse({
            "code": 60204,
            "message": "注册记录不存在"
        })
    algorithm = models.RecommendAlgorithm.objects.filter(watermark_type=record.watermark_type,
                                                         model_type=record.model_type)
    algorithm = models.WaterMarkAlgorithm.objects.get(algorithm_name=algorithm[0].algorithm_name)
    print(algorithm.verify_data_type)

    if algorithm.verify_data_type == 'API':
        return JsonResponse({
            "code": 60204,
            "message": "该注册记录应提交 API"
        })

    files = request.FILES.getlist("file", None)  # 接收前端传递过来的多个文件
    for file in files:
        sql_path = f"{os.getcwd()}/backend/judge_data/{hash}.{file.name.split('.')[1]}"
        with open(sql_path, 'wb') as f:
            for content in file.chunks():
                f.write(content)

        if file.name.split('.')[1] == 'zip':
            print("unzip")
            if not un_zip(sql_path, hash, 1):
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

        '''
        check data
        '''

    sql_path = f"{os.getcwd()}/backend/certification_data/{hash}"
    judge_path = f"{os.getcwd()}/backend/judge_data/{hash}"
    if os.path.isfile(f"{sql_path}/WhiteBoxVerify.py"):
        shutil.copy(f"{sql_path}/WhiteBoxVerify.py", f"{os.getcwd()}/backend/WhiteBoxVerify_curr.py")
    if os.path.isfile(f"{judge_path}/WhiteBoxExtract.py"):
        shutil.copy(f"{judge_path}/WhiteBoxExtract.py", f"{os.getcwd()}/backend/WhiteBoxExtract_curr.py")

    try:
        new_judge_data = models.JudgeData.objects.get(hash=hash)
    except:
        new_judge_data = models.JudgeData()
    new_judge_data.hash = hash
    new_judge_data.judge_data_path = judge_path
    new_judge_data.save()

    resp = {
        "code": 20000,
        "message": 'success',
    }
    return JsonResponse(resp)


@require_http_methods(["POST"])
def judge_apply(request):
    body_json = request.body.decode()
    body_dict = json.loads(body_json)
    token = body_dict['token']
    user = models.User.objects.get(token=token)
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
                result = 'success'
        except:
            return JsonResponse({
                "code": 60204,
                "message": "API Not Found"
            })
    else:
        sql_path = f"{os.getcwd()}/backend/certification_data/{hash}"
        judge_path = f"{os.getcwd()}/backend/judge_data/{hash}"

        qr_host = QRDataset(f"{sql_path}/index.txt", sql_path, torchvision.transforms.ToTensor())
        qr_host_loader = Data.DataLoader(
            dataset=qr_host,
            batch_size=16,
            shuffle=True
        )
        device = torch.device('cuda:2' if torch.cuda.is_available() else 'cpu')

        model3 = torch.load(f'{judge_path}/model/ResNet_extract.pkl').to(device)
        model4 = torch.load(f'{sql_path}/model/ResNet_verify.pkl').to(device)

        error_count = 0
        n = 0
        for step, (b_x, b_y) in enumerate(qr_host_loader):
            n += len(b_y)
            b_x = b_x.to(device)
            b_y = b_y.to(device)
            ans = model4(model3(b_x).to(device))
            for i in range(len(b_y)):
                if torch.argmax(ans[i]) != b_y[i]:
                    error_count = error_count + 1
        print(n)
        print(error_count / n * 100.0)
        result = 'success'

        with open(f"{os.getcwd()}/backend/WhiteBoxVerify_curr.py", 'w') as f:
            f.write("# initial WhiteBoxVerify")
        with open(f"{os.getcwd()}/backend/WhiteBoxExtract_curr.py", 'w') as f:
            f.write("# initial WhiteBoxExtract")

    judge_record = models.JudgeRecord()
    judge_record.hash = generate_key()
    judge_record.user_name = record.user_name
    judge_record.authentication_hash = hash
    if record.watermark_type == '黑盒':
        judge_record.judge_info = body_dict['api']
    else:
        # judge_data = models.JudgeData.objects.get(hash=hash)
        judge_record.judge_info = f"./backend/judge_data/{hash}"
        pass
    judge_record.judge_result = result
    judge_record.save()
    print(judge_record.timestamp)

    resp = {
        "code": 20000,
        "message": "success"
    }
    return JsonResponse(resp)


@require_http_methods(["GET"])
def judge_list(request):
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
        data = models.JudgeRecord.objects.filter(user_name=user.user_name)
    except models.JudgeRecord.DoesNotExist:
        return JsonResponse({
            "code": 60204,
            "message": "Record Not Found"
        })
    data = list(data.values())
    # print(data)
    for row in data:
        record = models.AuthenticationRecord.objects.get(hash=row['authentication_hash'])
        row['model_type'] = record.model_type
        row['watermark_type'] = record.watermark_type
        algorithm = models.RecommendAlgorithm.objects.filter(watermark_type=record.watermark_type,
                                                             model_type=record.model_type)
        algorithm = models.WaterMarkAlgorithm.objects.get(algorithm_name=algorithm[0].algorithm_name)
        row['algorithm_name'] = algorithm.algorithm_name
    resp = {
        "code": 20000,
        "data": data
    }
    return JsonResponse(resp)