from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Filter, Image

#フィルタオプション設定画面で使うフォーム
class DetailForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('img_src', 'user')
        labels = {
            'img_src': '入力画像',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()

class GrayForm(DetailForm):
    temp = 0 #構文エラー回避のために書いておく

class BlurForm(DetailForm):
    filter_size = forms.IntegerField(
        label = 'フィルタサイズ',
        required = True,
        min_value=1,
    )

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

#ログインするためのフォーム（LoginForm）はAuthenticationFormをそのまま使用する