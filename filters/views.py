from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.conf import settings

from .models import Filter, Image
from .forms import ImageForm

import cv2

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
        latest_img_id = Image.objects.latest('id').id
        latest_img = Image.objects.get(id=latest_img_id)
        input_path = settings.BASE_DIR + latest_img.img_src.url
        output_path = settings.BASE_DIR + '/image/output/output.jpg'
        print(output_path)
        gray(input_path, output_path) #仮の画像処理関数
        return HttpResponseRedirect(reverse('filters:index'))

def gray(input_path, output_path):
    img = cv2.imread(input_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(output_path, img_gray)