from django.db import models

from django.db import models
from django.utils import timezone

# Create your models here.
class Filter(models.Model):
    filter_name = models.CharField(max_length=200)
    filter_explain = models.CharField(max_length=200, default='')
    #オブジェクトにstrやprintを適用した場合に呼び出される（戻り値は文字列型）
    def __str__(self): 
        return self.filter_name

class Image(models.Model):
    img_src = models.ImageField(upload_to='.')
    img_opt = models.ImageField()