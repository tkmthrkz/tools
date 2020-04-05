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

class Option(models.Model):
    filter = models.ForeignKey(Filter, on_delete=models.CASCADE)
    option_name = models.CharField(max_length=200)

    def __str__(self):
        return self.option_name
