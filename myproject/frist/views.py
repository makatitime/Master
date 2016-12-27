from django.shortcuts import render
from django.http import HttpResponse
from .forms import InfoForms
# Create your views here.
def index(request):
    return render(request, 'index.html')
    #return HttpResponse('hello world')

def register(request):

    if request.method == 'POST':
        forms = InfoForms(request.POST)
        if forms.is_valid():
            pass
    else:
        forms = InfoForms()
        return render(request,'register.html',{'forms':forms.as_table() })

def login(request):
    return render(request,'login.html')