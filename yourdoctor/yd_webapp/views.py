from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


# example:
def index(request):

    context_dict={}
    context_dict['boldmessage']="Hello, this is an example."

    return render(request,'yd_webapp/index.html',context=context_dict)

def timetable(request):

    context_dict={}
    context_dict['doctor']="only doctor can access this page,for edit and choose"

    return render(request,'yd_webapp/timetable.html',context=context_dict)


