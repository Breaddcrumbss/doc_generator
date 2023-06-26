from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return(HttpResponse('Home'))


def upload(request):
    pass


def generate(request):
    pass