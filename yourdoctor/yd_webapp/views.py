from django.shortcuts import render, redirect
from django.http import HttpResponse
from yd_webapp import models
from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from django.db.models.query_utils import Q
from yd_webapp import models

# Create your views here.


# example:
def index(request):

    context_dict={}
    context_dict['boldmessage']="Hello, this is an example."

    return render(request,'yd_webapp/index.html',context=context_dict)


# to validate email address
def validate_email(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


# submit registration information


# ********************************************************
# ****************function of patients *******************
# ********************************************************


# user make an appointment
def booking(request):
    if request.method == 'GET':
        context_dict = {}
        context_dict['time_choices'] = models.Timetable.objects.filter(status=0)

        return render(request, 'yd_webapp/booking.html', context=context_dict)

    if request.method == 'POST':
        select_time = request.POST.get('availabletime')
        print(select_time)

    context_dict = {}
    context_dict['time_choices'] = models.Timetable.objects.filter(status=0)

    messages.success(request, "Your booking successed!")

    return render(request, 'yd_webapp/booking.html', context=context_dict)


# send messages and ask questions online
def ask_question(request):
    if request.method == 'POST':
        enter_email = request.POST.get('email')
        enter_question = request.POST.get('question')

        models.Record.objects.create(
            # this can be modified(?)
            patient_id=models.Patients.objects.get(patient_email=enter_email).patient_id,
            question_context=enter_question,
        )

    return HttpResponse("Please wait for the answer")


# show the records of the patient to give the feedback
def show_record(request):
    patient_id = ''
    records = models.Record.objects.filter(patient_id=patient_id)
    context_dict = {}
    context_dict['records'] = records
    return render(request, '', context=context_dict)


# give the feedback
def give_feedback(request):
    return render(request, '')


# ********************************************************
# ****************function of doctors *******************
# ********************************************************


# ？
def timetable(request):
    if request.method == 'GET':
        return render(request, 'yd_webapp/timetable.html')

    if request.method == 'POST':
        select_time = request.POST.get('gender')
        print(select_time)

    context_dict={}
    # context_dict['doctor']="only doctor can access this page,for edit and choose"

    return render(request,'yd_webapp/timetable.html',context=context_dict)


# get patient information
def useraccount(request):
    context_dict = {}

    if request.method == 'GET':
        return render(request, 'yd_webapp/patient.html', context=context_dict)

    if request.method == 'POST':
        user = models.Patients.objects.get(patient_id=2)

    return render(request,'yd_webapp/patient.html',context=context_dict)

# get doctor information
def doctoraccount(request):
    context_dict = {}

    if request.method == 'GET':
        return render(request, 'yd_webapp/doctor.html', context=context_dict)

    if request.method == 'POST':
        user = models.Patients.objects.get(patient_id=2)

    return render(request,'yd_webapp/doctor.html',context=context_dict)

# doctor edits timetable
def edittime(request):
    if request.method == 'GET':
        context_dict = {}
        times = models.Timetable.objects.filter(doctor_id=2).filter(status=0)
        timetable = []
        for i in times:
            print(i.time_id)
            timetable.append(i.time_id)
        context_dict['timetable'] = timetable
        return render(request, 'yd_webapp/edittime.html', context=context_dict)

    if request.method == 'POST':
        timetable = request.POST.getlist('time')
        timetable = [int(i) for i in timetable]
        print(timetable)

        for i in range(1, 6):
            if i in timetable:
                models.Timetable.objects.filter(doctor_id=2).filter(time_id=int(i)).update(status=0)
                print("updata 0")
            else:
                models.Timetable.objects.filter(doctor_id=2).filter(time_id=int(i)).update(status=1)
                print("updata 1")

    context_dict={}
    times = models.Timetable.objects.filter(doctor_id=2).filter(status=0)
    timetable = []
    for i in times:
        print(i.time_id)
        timetable.append(i.time_id)
    context_dict['timetable'] = timetable

    return render(request,'yd_webapp/edittime.html',context=context_dict)
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
        user=models.Doctors.objects.filter(doctor_email=request.POST.get('email'),doctor_psw=request.POST.get('password'))


        if len(list(user)) == 0:

            return render(request,'yd_webapp/doclogin.html',{'Error':'username do not exist'})
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
    return render(request,'yd_webapp/doctor.html',context=context_dict)



