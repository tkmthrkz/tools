from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView as LIV
from django.contrib.auth.views import LogoutView as LOV
from django.contrib.auth.views import auth_logout

import os
import shutil

from .models import Filter, Image
from .forms import *
from .filter_pro import Filter_pro #フィルタ処理実装部のインポート
from .const import *

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'filters/index.html'
    context_object_name = 'filter_list'

    def get_queryset(self): #コンテキスト変数に値をセットする関数
        return Filter.objects.filter().order_by('filter_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sessioninfo'] = self.request.session
        context['img_src'] = SAMPLE_IMG_SRC
        context['img_opt'] = SAMPLE_IMG_OPT
        return context

class DetailView(generic.DetailView): #DetailViewでは自動的にコンテキストにfiter変数が渡される
    model = Filter
    template_name = 'filters/detail.html'

    def get_queryset(self):
        return Filter.objects.filter() #コンテキスト変数に値をセットする関数

    def get_context_data(self, **kwargs): #コンテキスト変数の追加
        context = super().get_context_data(**kwargs)
        if 'username' in self.request.session:
            user_id = User.objects.get(username=self.request.session['username']).id
            ini_dict = { 'user': user_id }
        else:
            ini_dict ={ 'user': OTHER_ID }
        #フィルタにより分岐
        if self.kwargs['pk'] == FILTER_NAME2PK['gray']: #グレースケール処理の場合
            context['form'] = GrayForm(initial=ini_dict)
        elif self.kwargs['pk'] == FILTER_NAME2PK['blur']:
            context['form'] = BlurForm(initial=ini_dict)
        return context

def apply(request, filter_name):
    if request.method == 'POST':
        form = DetailForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            inputimg_name = request.FILES['img_src'].name
            outputimg_name = 'output_' + request.FILES['img_src'].name
            if 'username' in request.session:
                user_id = request.session['userid']
                image = Image.objects.filter(user_id=user_id).order_by('-id')[0]
                image.img_src_name = inputimg_name
                image.img_opt = 'output/{}/{}'.format(user_id, outputimg_name)
                image.img_opt_name = outputimg_name
                image.save()

                input_path  = settings.MEDIA_ROOT + '/upload/{}/{}'.format(user_id, inputimg_name)
                output_path = settings.MEDIA_ROOT + '/output/{}/{}'.format(user_id, outputimg_name) 

            else:
                image = Image.objects.filter(user_id=OTHER_ID).order_by('-id')[0]
                image.img_src_name = inputimg_name
                image.img_opt = 'output/{}/{}'.format(str(OTHER_ID), outputimg_name)
                image.img_opt_name = outputimg_name
                image.save()

                input_path =  settings.MEDIA_ROOT + '/upload/{}/{}'.format(OTHER_ID, inputimg_name)
                output_path = settings.MEDIA_ROOT + '/output/{}/{}'.format(OTHER_ID, outputimg_name)

            filter_pro = Filter_pro(input_path, output_path)
            
            if filter_name == GRAY:
                filter_pro.gray() #ファイル書き出しまで行う
            elif filter_name == BLUR:
                filter_size = int(form.data['filter_size'])
                filter_pro.blur(filter_size) #ファイル書き出しまで行う
            return HttpResponseRedirect(reverse('filters:result', kwargs=dict(filter_name=filter_name)))
        return redirect(reverse('filters:detail', kwargs=dict(pk=FILTER_NAME2PK[filter_name])))
    return redirect(reverse('filters:detail', kwargs=dict(pk=FILTER_NAME2PK[filter_name])))

class ResultView(generic.TemplateView):
    template_name = 'filters/result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sessioninfo'] = self.request.session
        if  'username' in self.request.session:
            context['image'] = Image.objects.filter(user_id=self.request.session['userid']).order_by('-id')[0]
        else:
            context['image'] = Image.objects.filter(user_id=OTHER_ID).order_by('-id')[0]
        return context

class chmView(generic.ListView): #変換履歴管理画面
    template_name = 'filters/chm.html'
    context_object_name = 'image_list'

    def get_queryset(self):  # コンテキスト変数に値をセットする関数
        user_id = self.request.session['userid']
        return Image.objects.filter(user_id=user_id)

class SignupView(generic.CreateView):
    form_class = SignupForm
    template_name = 'filters/signup.html'
    success_url = reverse_lazy('filters:index')

    def form_valid(self, form): #バリデーションが有効の時、呼び出される
        user = form.save()
        login(self.request, user)
        user_id = str(User.objects.get(username=user.username).id)
        user_name = form.cleaned_data.get('username')
        self.request.session['userid']   = user_id
        self.request.session['username'] = user_name
        os.makedirs(settings.MEDIA_ROOT + '/output/{}'.format(user_id), exist_ok=True)
        os.makedirs(settings.MEDIA_ROOT + '/upload/{}'.format(user_id),  exist_ok=True)
        self.object = user        
        return HttpResponseRedirect(self.get_success_url())

class LoginView(LIV):
    form_class = AuthenticationForm
    template_name = 'filters/login.html'
    success_url = reverse_lazy('filters:index')

    def form_valid(self, form):
        user_name = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=user_name, password=password)
        if user is not None:
            login(self.request, user)
            user_id = str(User.objects.get(username=user_name).id)
            self.request.session['userid']   = user_id
            self.request.session['username'] = user_name
            os.makedirs(settings.MEDIA_ROOT + '/upload/{}'.format(user_id),  exist_ok=True) 
            os.makedirs(settings.MEDIA_ROOT  + '/output/{}'.format(user_id), exist_ok=True) 
            return HttpResponseRedirect(self.get_success_url())
 
class LogoutView(LOV):
    template_name = 'filters/logout.html'

class LeavecheckView(generic.TemplateView):
    template_name = 'filters/leavecheck.html'

def leave(request):
    user_id = request.user.id
    user = User.objects.filter(id=user_id)
    shutil.rmtree(settings.MEDIA_ROOT + '/upload/{}'.format(user_id))
    shutil.rmtree(settings.MEDIA_ROOT + '/output/{}'.format(user_id))
    user.delete()
    auth_logout(request)
    return redirect(reverse('filters:index'))
