from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.conf import settings

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
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('filters:apply', kwargs=dict(filter_name=filter_name)))
    else:
        form = ImageForm()
        filter_pro = Filter_pro()
        if filter_name == filter_nametoname['gray']:
            filter_pro.gray()
        elif filter_name == filter_nametoname['blur']: #ガウシアン
            filter_pro.blur(3)
        return HttpResponseRedirect(reverse('filters:index'))