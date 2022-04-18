from __future__ import unicode_literals

from django.db import models
  
 # Create your models here.

def upload_location(instance, filename):    #图片改名函数
    filebase, extension = filename.split('.')
    return 'images/%s.%s' % (instance.account_walletaddress, extension)

class   Account(models.Model):
    account_name = models.CharField(max_length=64)
    account_type = models.IntegerField() #0为公司 1为用户
    #图片存储路径：media/images文件夹下，图片名为钱包名
    #不输入钱包名的话图片名为NULL，钱包名重复的话会附加一串乱码
    account_img = models.ImageField(upload_to=upload_location)  
    account_password1 = models.CharField(max_length=64)
    account_password2 = models.CharField(max_length=64)
    account_ifreserve = models.BooleanField(default=False) #是否订票
    account_walletaddress = models.CharField(max_length=64,default='no') #钱包地址

class   Ticket(models.Model):
    ticket_num = models.IntegerField(default=64) #Ticket总数，初始化为64
    ticket_name = models.CharField(max_length=64,default="ticket")
