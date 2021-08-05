from django.contrib.auth.backends import ModelBackend
from django.db.models.query_utils import Q
from yd_webapp import models

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
# Create your views here.



def index(request):
    pass
    return render(request,'yd_webapp/index.html')

def user_login(request):
    if request.method =="POST":

        # username = request.POST.get('id')
        # password = request.POST.get('password')
        # user = authenticate(Patients_id=username, patient_psw=password)    
        user=models.Patients.objects.filter(patient_email=request.POST.get('email'),patient_psw=request.POST.get('password'))
        
        
        if len(list(user)) == 0:
        
            return render(request,'yd_webapp/login.html',{'Error':'username do not exist'})
        else:
            request.session.set_expiry(3000)  #Session Authentication duration is 3000s. After 3000s, the session authentication becomes invalid
            # login(request,user)
            request.session['username']=request.POST.get('email')   #user的值发送给session里的username
            request.session['is_login']=True   #认证为真
            # return request.session['is_login']
            
            # return HttpResponse(request.session['is_login'])
            # return redirect('yd_webapp:index')
            return redirect('yd_webapp:index')
    else:
        return render(request,'yd_webapp/login.html')
def doc_login(request):
    if request.method =="POST":

        # username = request.POST.get('id')
        # password = request.POST.get('password')
        # user = authenticate(Patients_id=username, patient_psw=password)    
        user=models.Patients.objects.filter(doctor_id=request.POST.get('id'),doctor_psw=request.POST.get('password'))
        
        
        if len(list(user)) == 0:
        
            return render(request,'yd_webapp/doclogin.html',{'Error':'username do not exist'})
        else:
            request.session.set_expiry(3000)  #Session Authentication duration is 3000s. After 3000s, the session authentication becomes invalid
            # login(request,user)
            request.session['username']=request.POST.get('id')   #user的值发送给session里的username
            request.session['is_login']=True   #认证为真
            # return request.session['is_login']
            
            # return HttpResponse(request.session['is_login'])
            # return redirect('yd_webapp:index')
            return redirect('yd_webapp:index')
    else:
        return render(request,'yd_webapp/doclogin.html')        

def register(request):
    pass
    return render(request,'yd_webapp/register.html')

def user_logout(request):
    request.session.clear() 
    print("1111")
    return redirect('yd_webapp:index')
def user_register(request):
    
    if request.method =="POST":
        user=models.Patients.objects.filter(patient_id=request.POST.get('id'),patient_psw=request.POST.get('password'))
        if len(list(user)) == 0:
            models.Patients.objects.create(
                patient_id=request.POST.get('id'),
                patient_name=request.POST.get('username'),
                patient_email=request.POST.get('email'),
                patient_gender=request.POST.get('gender'),
                patient_phone_num=request.POST.get('phonenumber'),
                patient_psw=request.POST.get('password'),
                address=request.POST.get('address'),
                patient_age=request.POST.get('age'),

            )
            return render(request,'yd_webapp/index.html')
        else:
            return HttpResponse("userid does exist")
    else:
    
        return render(request,'yd_webapp/register.html')



