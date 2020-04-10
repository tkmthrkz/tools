from django import forms
from .models import Filter, Image

class BaseForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('img_src', )
        labels = {
            'img_src': '入力画像',
        }

class GrayForm(BaseForm):
    temp = 0 #構文エラー回避のために書いておく

class BlurForm(BaseForm):
    filter_size = forms.IntegerField(
        label = 'フィルタサイズ',
        required = True,
        min_value=1,
    )
