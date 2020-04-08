from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.conf import settings

from .models import Filter, Image
from .forms import ImageForm
from .filter_pro import Filter_pro #フィルタ処理実装部のインポート

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ImageForm()
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
        if filter_name == 'gray':
            filter_pro.gray()
        elif filter_name == 'blur': #ガウシアン
            filter_pro.blur(3)
        return HttpResponseRedirect(reverse('filters:index'))