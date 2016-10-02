from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
	#return HttpResponse('hello test123')
	return render(request,'home.html')

def add(request):
	a = request.GET['a']
	b = request.GET['b']
	c = int(a) + int(b)
	return HttpResponse(str(c))

def  add2(request,a,b):
	s = int(a) + int(b)
	return HttpResponse(str(s))

