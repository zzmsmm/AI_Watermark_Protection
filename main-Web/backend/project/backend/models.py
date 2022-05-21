from django.db import models

MEDIA_ADDR = "http://localhost:8000/media/"
# Create your models here.


class User(models.Model):
    user_name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    token = models.CharField(max_length=256, null=True)
    email = models.CharField(max_length=128, null=True)
    # avatar = models.CharField(max_length=128, null=True)
    avatar = models.ImageField(upload_to='avatar', default='', null=True)

    def __str__(self) -> str:
        return self.user_name

    def get_avatar_url(self):
        return MEDIA_ADDR + str(self.avatar)


# 水印算法表
class WaterMarkAlgorithm(models.Model):
    algorithm_name = models.CharField(max_length=128, unique=True)
    algorithm_detail = models.CharField(max_length=128, null=True)
    key_generate = models.CharField(max_length=128, null=True)
    authentication_data_type = models.CharField(max_length=128, null=True)
    verify_data_type = models.CharField(max_length=128, null=True)

    def __str__(self) -> str:
        return self.algorithm_name


# 推荐水印算法表
class RecommendAlgorithm(models.Model):
    watermark_type = models.CharField(max_length=128, null=True)
    model_type = models.CharField(max_length=128, null=True)
    algorithm_name = models.CharField(max_length=128, null=True)


# 认证数据表
class AuthenticationData(models.Model):
    hash = models.CharField(max_length=128, unique=True)
    authentication_data_path = models.CharField(max_length=128, null=True)

    def __str__(self) -> str:
        return self.hash


# 裁决数据表
class JudgeData(models.Model):
    hash = models.CharField(max_length=128, unique=True)
    judge_data_path = models.CharField(max_length=128, null=True)

    def __str__(self) -> str:
        return self.hash


# 认证记录表
class AuthenticationRecord(models.Model):
    user_name = models.CharField(max_length=128)
    hash = models.CharField(max_length=128, unique=True)
    watermark_type = models.CharField(max_length=128, null=True)
    model_type = models.CharField(max_length=128, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    key = models.CharField(max_length=128, null=True)

    def __str__(self) -> str:
        return self.hash

    def keys(self):
        return ('user_name', 'hash', 'watermark_type', 'model_type', 'timestamp', 'key')

    def __getitem__(self, item):
        return getattr(self, item)


# 裁决记录表
class JudgeRecord(models.Model):
    user_name = models.CharField(max_length=128)
    hash = models.CharField(max_length=128, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    authentication_hash = models.CharField(max_length=128, null=True)
    judge_info = models.CharField(max_length=128, null=True)
    judge_result = models.CharField(max_length=128, null=True)

    def __str__(self) -> str:
        return self.hash

    def keys(self):
        return ('user_name', 'hash', 'timestamp', 'authentication_hash',
                'judge_info', 'judge_result')

    def __getitem__(self, item):
        return getattr(self, item)


# 待完成认证请求信息表
class RequestInfo(models.Model):
    user_name = models.CharField(max_length=128)
    hash = models.CharField(max_length=128, unique=True)
    watermark_type = models.CharField(max_length=128, null=True)
    model_type = models.CharField(max_length=128, null=True)
    key = models.CharField(max_length=128, null=True)

    def __str__(self) -> str:
        return self.hash

    def keys(self):
        return 'user_name', 'hash', 'watermark_type', 'model_type', 'key'

    def __getitem__(self, item):
        return getattr(self, item)