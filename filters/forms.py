from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Filter, Image, User

#フィルタオプション設定画面で使うフォーム
class DetailForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('img_src', )
        labels = {
            'img_src': '入力画像',
        }

class GrayForm(DetailForm):
    temp = 0 #構文エラー回避のために書いておく

class BlurForm(DetailForm):
    filter_size = forms.IntegerField(
        label = 'フィルタサイズ',
        required = True,
        min_value=1,
    )

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('user_name', 'password1', 'password2')