from django.shortcuts import render
from django.http import  Http404
from django.http import HttpResponse
from  django.http import HttpResponseRedirect
from .models import articles
from .forms import ArtForms
import hashlib
# Create your views here.
# def index_page(request):
#     d = request.META
#     meta = d.items()
#     meta.sort()
#     return render(request,'index.html',{ 'meta':meta })
def index_page(request):
    response3 = articles.objects.all()
    return render(request,'index.html',{'all_response':response3})
def  detail(request,nid):
    response3 = articles.objects.filter(id=nid)
    #return HttpResponse(nid)
    return render(request,'index.html',{'all_response':response3})
def  delete(request,id):
    response = articles.objects.filter(id=id)
    print len(response)
    response3 = response.delete()
    print len(response)
    #print response3
    if  len(response) == 0:
        return HttpResponse('Fail')
    else:
        #response.delete()
        return HttpResponse('Success')


def add_page(request):
    if request.method == 'POST':
        form = ArtForms(request.POST)
        if form.is_valid():
            #print form
            at = form.cleaned_data['name']
            tt = form.cleaned_data['title']
            cc = form.cleaned_data['content']
            mail = form.cleaned_data['email']
            ars = articles.objects.create(author=at,title=tt,content=cc,email=mail)
            ars.save()
            return HttpResponseRedirect("/")
        else:
            er = form.errors
            return render(request,'error.html',{'errs':er})
            #return HttpResponse(form.errors.as_data())
    else:
        forms = ArtForms()
        return render(request,'add.html',{'form':forms.as_p()})

def register(request):
    if request.method == 'POST':
        form = AddForm(request.POST)

        if form.is_valid():
            m = hashlib.md5()
            username  = form.cleaned_data['username']
            password = hashlib.md5(form.cleaned_data['password'])
            password = password.hexdigest()
            email = form.cleaned_data['Email']
            gender = form.cleaned_data['Gender']
            age = 23
            res = Author.objects.create(username=username,password=password,age=age,sex=gender)
            res.save
            return HttpResponse(password)
        else:
            print 'hehe'

    else:
        form = AddForm()
        return  render(request,'register.html',{'form': form })
