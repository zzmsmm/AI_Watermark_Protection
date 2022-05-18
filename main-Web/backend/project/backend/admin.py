from django.contrib import admin

# Register your models here.
from . import models
admin.site.register(models.User)
admin.site.register(models.WaterMarkAlgorithm)
admin.site.register(models.RequestInfo)
admin.site.register(models.RecommendAlgorithm)
admin.site.register(models.AuthenticationRecord)
admin.site.register(models.AuthenticationData)
admin.site.register(models.JudgeData)