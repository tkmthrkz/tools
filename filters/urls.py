from django.urls import path
from . import views

app_name = 'filters'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'), #フィルタ効果トップ
    path('<int:pk>', views.DetailView.as_view(), name='detail'), #均一ぼかし
]