from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def posts_create(request):
    return HttpResponse("<h1>CREATE</h1")

def posts_detail(request):
    return HttpResponse("<h1>RETRIEVE (ONE)</h1")

def posts_list(request):
    return HttpResponse("<h1>RETRIEVE (LIST)</h1")

def posts_update(request):
    return HttpResponse("<h1>UPDATE</h1")

def posts_delete(request):
    return HttpResponse("<h1>DELETE</h1")
