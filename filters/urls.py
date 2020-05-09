from django.urls import path
#from django.conf.urls.static import static
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from . import views

app_name = 'filters'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'), #フィルタ選択
    path('<int:pk>', views.DetailView.as_view(), name='detail'), #フィルタ詳細
    path('<str:filter_name>/apply/', views.apply, name='apply'), #フィルタ適用
    path('<str:filter_name>/apply/result/', views.ResultView.as_view(), name='result'), #適用後の画像ダウンロード画面
    path('signup/', views.SignupView.as_view(), name='signup'), #サインアップ画
    path('login/', views.LoginView.as_view(), name='login'), #ログイン画面
    path('logout/', views.LogoutView.as_view(), name='logout'), #ログアウト画面
    path('leavecheck/', views.LeavecheckView.as_view(), name='leavecheck'),
    path('leavecheck/leave/', views.leave, name='leave'),
    path('chm/', views.chmView.as_view(), name='chm'), #変換履歴管理画面
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)