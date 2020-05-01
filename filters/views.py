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
import tkinter
from tkinter import filedialog

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
        return context

class DetailView(generic.DetailView): #DetailViewでは自動的にコンテキストにfiter変数が渡される
    model = Filter
    template_name = 'filters/detail.html'

    def get_queryset(self):
        return Filter.objects.filter() #コンテキスト変数に値をセットする関数

    def get_context_data(self, **kwargs): #コンテキスト変数の追加
        context = super().get_context_data(**kwargs)
        if 'username' in self.request.session:
            ini_dict = { 'user': User.objects.get(username=self.request.session['username']) }
        else:
            ini_dict ={ 'user': OTHER_ID }
        #フィルタにより分岐
        if self.kwargs['pk'] == FILTER_PK['gray']: #グレースケール処理の場合
            context['form'] = GrayForm(initial=ini_dict)
        elif self.kwargs['pk'] == FILTER_PK['blur']:
            context['form'] = BlurForm(initial=ini_dict)
        return context

def apply(request, filter_name):
    if request.method == 'POST':
        form = DetailForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if 'username' in request.session:
                image = Image.objects.filter(user_id=request.session['userid']).order_by('-id')[0]
                image.img_opt = 'output/{}/output.jpg'.format(request.session['userid'])
                image.save()
            else:
                image = Image.objects.filter(user_id=OTHER_ID).order_by('-id')[0]
                image.img_opt = 'output/{}/output.jpg'.format(str(OTHER_ID))
                image.save()

            if 'username' in request.session:
                input_path  = settings.MEDIA_ROOT + '/upload/{}/{}'.format(request.session['userid'], request.FILES['img_src'].name)
                output_path = settings.MEDIA_ROOT + '/output/{}/output.jpg'.format(request.session['userid']) 
            else:
                input_path =  settings.MEDIA_ROOT + '/upload/24/{}'.format(request.FILES['img_src'].name)
                output_path = settings.MEDIA_ROOT + '/output/24/output.jpg'
            filter_pro = Filter_pro(input_path, output_path)
            
            if filter_name == filter_nametoname['gray']:
                filter_pro.gray() #ファイル書き出しまで行う
            elif filter_name == filter_nametoname['blur']:
                filter_size = int(form.data['filter_size'])
                filter_pro.blur(filter_size) #ファイル書き出しまで行う
            return HttpResponseRedirect(reverse('filters:result', kwargs=dict(filter_name=filter_name)))
        return redirect(reverse('filters:detail', kwargs=dict(filter_name=FILTER_PK[filter_name])))
    return redirect(reverse('filters:detail', kwargs=dict(filter_name=FILTER_PK[filter_name])))

class ResultView(generic.TemplateView):
    template_name = 'filters/result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sessioninfo'] = self.request.session
        context['media_url'] = settings.MEDIA_URL
        if  'username' in self.request.session:
            context['image'] = Image.objects.filter(user_id=self.request.session['userid']).order_by('-id')[0]
        else:
            context['image'] = Image.objects.filter(user_id=OTHER_ID).order_by('-id')[0]
        # if 'userid' in self.request.session:
        #     output_url = os.path.join(settings.MEDIA_ROOT, 'output', self.request.session['userid'], 'output.jpg')
        #     context['output_url'] = output_url
        # else:
        #     output_url = os.path.join(settings.MEDIA_ROOT, 'output', str(OTHER_ID), 'output.jpg') 
        #     context['output_url'] = output_url
        return context

class SignupView(generic.CreateView):
    form_class = SignupForm
    template_name = 'filters/signup.html'
    success_url = reverse_lazy('filters:index')

    def form_valid(self, form): #バリデーションが有効の時、呼び出される
        user = form.save()
        login(self.request, user)
        self.request.session['userid']   = str(User.objects.get(username=user.username).id)
        self.request.session['username'] = form.cleaned_data.get('username')
        os.makedirs(settings.MEDIA_ROOT + '/output/{}'.format(self.request.session['userid']), exist_ok=True)
        os.makedirs(settings.MEDIA_ROOT + '/upload/{}'.format(self.request.session['userid']),  exist_ok=True)
        self.object = user        
        return HttpResponseRedirect(self.get_success_url())

class LoginView(LIV):
    form_class = AuthenticationForm
    template_name = 'filters/login.html'
    success_url = reverse_lazy('filters:index')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            self.request.session['userid']   = str(User.objects.get(username=username).id)
            self.request.session['username'] = username
            os.makedirs(settings.MEDIA_ROOT + '/upload/{}'.format(self.request.session['userid']),  exist_ok=True) 
            os.makedirs(settings.MEDIA_ROOT  + '/output/{}'.format(self.request.session['userid']), exist_ok=True) 
            return HttpResponseRedirect(self.get_success_url())
 
class LogoutView(LOV):
    template_name = 'filters/logout.html'

class LeavecheckView(generic.TemplateView):
    template_name = 'filters/leavecheck.html'

def leave(request):
    user = User.objects.filter(id=request.user.id)
    shutil.rmtree(settings.MEDIA_ROOT + '/upload/{}'.format(request.session['userid']))
    shutil.rmtree(settings.MEDIA_ROOT + '/output/{}'.format(request.session['userid']))
    user.delete()
    auth_logout(request)
    return redirect(reverse('filters:index'))