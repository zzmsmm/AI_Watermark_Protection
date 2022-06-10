from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.shortcuts import HttpResponse
import json
import hashlib
from . import models


@require_http_methods(["GET"])
def get_count(request):
    token = request.GET.get("token")
    try:
        user = models.User.objects.get(token=token)
    except:
        return JsonResponse({
            "code": 60204,
            "message": "not_exist"
        })
    if user.user_name != "admin":
        return JsonResponse({
            "code": 60204,
            "message": "不可查看"
        })
    user_num = models.User.objects.all().count() - 1
    algorithm_num = models.WaterMarkAlgorithm.objects.all().count()
    authentication_num = models.AuthenticationRecord.objects.all().count()
    judge_num = models.JudgeRecord.objects.all().count()
    resp = {
        "code": 20000,
        "data": {
            "user_num": user_num,
            "algorithm_num": algorithm_num,
            "authentication_num": authentication_num,
            "judge_num": judge_num
        }
    }
    return JsonResponse(resp)
