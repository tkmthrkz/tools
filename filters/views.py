from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.views.generic import CreateView
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import login, authenticate

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
    
class DetailView(generic.DetailView): #DetailViewでは自動的にコンテキストにfiter変数が渡される
    model = Filter
    template_name = 'filters/detail.html'

    def get_queryset(self):
        return Filter.objects.filter() #コンテキスト変数に値をセットする関数

    def get_context_data(self, **kwargs): #コンテキスト変数の追加
        context = super().get_context_data(**kwargs)
        #フィルタにより分岐
        #filter_pk = {'blur': 2, 'gray': 3, }
        if self.kwargs['pk'] == filter_pk['gray']: #グレースケール処理の場合
            context['form'] = GrayForm()
        elif self.kwargs['pk'] == filter_pk['blur']:
            context['form'] = BlurForm()
        return context
    

def apply(request, filter_name):
    print('request = {} filter_name = {}'.format(request, filter_name))
    if request.method == 'POST':
        form = DetailForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            input_path = settings.BASE_DIR + '/image/upload/' + request.FILES['img_src'].name
            #output_path = filedialog.askdirectory(title='出力先を選択してください')
            output_path = settings.BASE_DIR + '/image/output/output.jpg' #tkinterで解決できないエラーを解決するまでの仮パス
            filter_pro = Filter_pro(input_path, output_path)
            
            if filter_name == filter_nametoname['gray']:
                filter_pro.gray() #ファイル書き出しまで行う
            elif filter_name == filter_nametoname['blur']:
                filter_size = int(form.data['filter_size'])
                filter_pro.blur(filter_size) #ファイル書き出しまで行う
            return HttpResponseRedirect(reverse('filters:index'))
    return redirect(reverse('filters:detail', kwargs=dict(filter_name=filter_pk[filter_name])))

class SignupView(CreateView):
    def post(self, request, *args, **kwargs): #POST時に自動で呼び出される
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('user_name')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('filters:index'))
        return render(request, 'filters/signup.html', {'form': form, })
    
    def get(self, request, *args, **kwargs):
        form = SignupForm(request.POST)
        return render(request, 'filters/signup.html', {'form': form, })