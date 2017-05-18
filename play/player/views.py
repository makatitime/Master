from django.shortcuts import render
from django.http import  Http404
from django.http import HttpResponse
from  django.http import HttpResponseRedirect
from .models import articles
from .forms import ArtForms
# Create your views here.
# def index_page(request):
#     d = request.META
#     meta = d.items()
#     meta.sort()
#     return render(request,'index.html',{ 'meta':meta })
def index_page(request):
    response3 = articles.objects.all()
    return render(request,'index.html',{'all_response':response3})

def add_page(request):
    if request.method == 'POST':
        at = request.POST['author']
        tt = request.POST['title']
        cc = request.POST['content']
        ars = articles.objects.create(author=at,title=tt,content=cc)
        ars.save()
        return HttpResponseRedirect("/")
    else:
        forms = ArtForms()
        return render(request,'add.html',{'form':forms})
