from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


# example:
def index(request):
    return HttpResponse("Hello, this is an example.")



