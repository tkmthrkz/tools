from django.db import models

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

import os

from .const import SUPPORT_EXT

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


def validate_is_picture(value):
    ext = os.path.splitext(value.name)[1]

    if not ext.lower() in SUPPORT_EXT:
        raise ValidationError('Only picure files are availables.')
def get_upload_to(self, file_name): #アップロード先のディレクトリを示す
    return os.path.join('upload', str(self.user_id), file_name)
class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    img_src = models.ImageField(
        upload_to=get_upload_to, validators=[validate_is_picture])
    img_src_name = models.CharField(max_length=100, default='img_src')
    img_opt = models.ImageField()
    img_opt_name = models.CharField(max_length=100, default='img_opt')
    date = models.DateTimeField(default=timezone.now)
