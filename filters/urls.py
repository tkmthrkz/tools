from django.urls import path
from . import views

app_name = 'filters'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'), #フィルタ選択
    path('<int:pk>', views.DetailView.as_view(), name='detail'), #フィルタ詳細
    path('<str:filter_name>/apply/', views.apply, name='apply'), #フィルタ適用
    path('signup/', views.SignupView.as_view(), name='signup'), #サインアップ画面
]