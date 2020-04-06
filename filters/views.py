from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.conf import settings

from .models import Filter, Image
from .forms import ImageForm

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

    

def apply(request, filter_name):
    print('request = {} filter_name = {}'.format(request, filter_name))
    print(request.POST.get('imgfile'))
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('filters:apply')
    else:
        form = ImageForm()
        latest_img_id = Image.object.latest('id').id
        latest_img = Image.object.get(id=latest_img_id)
        input_path = settings.BASE_DIR + latest_img.img_src.url
        output_path = settings.BASE_DIR + '/output/output.jpg'
        #処理関数を書く
    
    # try:
    # except: #なんらかのエラーが発生した場合
    #     return render(request, 'filters/detail.html', {
    #         'filter': filter_name, 
    #         'error_message': 'もう一度ファイルを選択してください', 
    #         })
    # else: #ファイルが選択されている場合
    #     print(request.POST['imgfile'])

    return HttpResponseRedirect(reverse('filters:index'))