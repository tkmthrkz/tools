from django.db import models

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

import os

# Create your models here.
class Filter(models.Model):
    filter_name = models.CharField(max_length=200)
    filter_explain = models.CharField(max_length=200, default='')
    #オブジェクトにstrやprintを適用した場合に呼び出される（戻り値は文字列型）
    def __str__(self): 
        return self.filter_name

class Option(models.Model):
    filter = models.ForeignKey(Filter, on_delete=models.CASCADE)
    option_name = models.CharField(max_length=100) #フィルタのオプション名
    
    def __str__(self):
        return self.option_name


def get_upload_to(self, file_name):
    return os.path.join('./upload', str(self.user_id), file_name)

class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    img_src = models.ImageField(upload_to=get_upload_to)
    img_opt = models.ImageField()

