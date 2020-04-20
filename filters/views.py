from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import CreateView
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView as LIV
from django.contrib.auth.views import LogoutView as LOV

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
        context['session'] = self.request.session
        return context

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
    form_class = SignupForm
    template_name = 'filters/signup.html'
    success_url = reverse_lazy('filters:index')

    def form_valid(self, form): #バリデーションが有効の時、呼び出される
        user = form.save()
        login(self.request, user)

        self.request.session['username'] = self.object.username

        return HttpResponseRedirect(self.get_success_url())

    # def post(self, request, *args, **kwargs): #POST時に自動で呼び出される
    #     form = SignupForm(data=request.POST)
    #     if form.is_valid():
    #         form.save()
    #         username = form.cleaned_data.get('username')
    #         password = form.cleaned_data.get('password1')
    #         user = authenticate(username=username, password=password)
    #         login(request, user)
    #         return redirect(reverse('filters:index'))
    #     return render(request, 'filters/signup.html', {'form': form, })
    
    # def get(self, request, *args, **kwargs):
    #     form = SignupForm(request.POST)
    #     return render(request, 'filters/signup.html', {'form': form, })

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
            self.request.session['username'] = username
            return HttpResponseRedirect(self.get_success_url())
 
class LogoutView(LOV):
    template_name = 'filters/logout.html'