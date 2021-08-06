from django.shortcuts import render, redirect
from django.http import HttpResponse
from yd_webapp import models
from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from django.db.models.query_utils import Q
from yd_webapp import models
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.forms.models import model_to_dict

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
        # availabletime is the t_id in the timetable which is available
        select_t_id = request.POST.get('availabletime')

        # the time record object that the patient choose
        select_time = models.Timetable.objects.get(t_id=int(select_t_id))
        patient = models.Patients.objects.get(patient_id=request.session.get('user_id'))

        # updata the timetable after booking
        models.Timetable.objects.filter(t_id=int(select_t_id)).update(status=1)
        models.Booking.objects.create(
            patient_id=patient,
            t_id=select_time,
        )
        print("Booking succeed")

        messages.success(request, 'Your book is accepted! ')
        return redirect('/yd_webapp/patient/')

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
        doctor_id = request.session.get('user_id')


        context_dict = {}
        times = models.Timetable.objects.filter(doctor_id=doctor_id).filter(status=0)
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


# patients log in
def user_login(request):
    if request.method =="POST":

        # username = request.POST.get('id')
        # password = request.POST.get('password')
        # user = authenticate(Patients_id=username, patient_psw=password)
        user = models.Patients.objects.get(patient_email=request.POST.get('email'), patient_psw=request.POST.get('password'))
        if not user:
            return render(request,'yd_webapp/login.html',{'Error':'username do not exist'})
        else:
            request.session.set_expiry(3000)  #Session Authentication duration is 3000s. After 3000s, the session authentication becomes invalid
            # login(request,user)
            request.session['is_login'] = True  # 认证为真
            request.session['user_id'] = user.patient_id
            request.session['user_name'] = user.patient_name   #user的值发送给session里的username
            request.session['user_gender'] = user.patient_gender
            request.session['user_age'] = user.patient_age
            request.session['user_adderess'] = user.address
            request.session['user_email'] = user.patient_email
            request.session['user_phone'] = user.patient_phone_num

            return redirect('yd_webapp:user')
    else:
        return render(request,'yd_webapp/login.html')


# doctors log in
def doc_login(request):
    if request.method =="POST":

        # username = request.POST.get('id')
        # password = request.POST.get('password')
        # user = authenticate(Patients_id=username, patient_psw=password)
        user = models.Doctors.objects.get(doctor_email=request.POST.get('email'),doctor_psw=request.POST.get('password'))

        if not user:
            return render(request,'yd_webapp/doclogin.html',{'Error':'username do not exist'})
        else:
            request.session.set_expiry(3000)  #Session Authentication duration is 3000s. After 3000s, the session authentication becomes invalid
            # login(request,user)
            request.session['username'] = request.POST.get('email')   #user的值发送给session里的username
            request.session['is_login']=True   #认证为真
            request.session['user_id'] = user.doctor_id
            request.session['user_name'] = user.doctor_name  # user的值发送给session里的username
            request.session['user_email'] = user.doctor_email

            # return HttpResponse(request.session['is_login'])
            # return redirect('yd_webapp:index')
            return redirect('yd_webapp:doctor')
    else:
        return render(request,'yd_webapp/doclogin.html')


def user_logout(request):
    request.session.clear()
    print("Log out")
    return redirect('yd_webapp:index')


# submit registration information
def user_register(request):

    if request.method == 'POST':
        enter_email = request.POST.get('email')
        enter_name = request.POST.get('username')
        enter_age = request.POST.get('age')
        enter_gender = request.POST.get('gender')
        enter_phone = request.POST.get('phonenumber')
        enter_address = request.POST.get('address')
        enter_password = request.POST.get('password')
        enter_confirm_pwd = request.POST.get('confirm_pwd')

        # Determine whether any received data is empty
        if not enter_email.strip():
            error_message = "Email can not be empty"
            return render(request, 'yd_webapp/register.html', locals())
        elif not enter_name.strip():
            error_message = "Name can not be empty"
            return render(request, 'yd_webapp/register.html', locals())
        elif not enter_age.strip():
            error_message = "Age can not be empty"
            return render(request, 'yd_webapp/register.html', locals())
        elif not enter_gender.strip():
            error_message = "Gender can not be empty"
            return render(request, 'yd_webapp/register.html', locals())
        elif not enter_phone.strip():
            error_message = "Phone number can not be empty"
            return render(request, 'yd_webapp/register.html', locals())
        elif not enter_address.strip():
            error_message = "Address can not be empty"
            return render(request, 'yd_webapp/register.html', locals())
        elif not enter_password.strip():
            error_message = "Password can not be empty"
            return render(request, 'yd_webapp/register.html', locals())
        elif not enter_confirm_pwd.strip():
            error_message = "Confirm password can not be empty"
            return render(request, 'yd_webapp/register.html', locals())

        # Determine email format and password and confirm_password whether same
        if not validate_email(enter_email):
            error_message = "Email format is wrong!"
            return render(request, 'yd_webapp/register.html', locals())
        elif len(enter_password) < 8:
            error_message = "Password length must not be less than 8 characters!"
        elif enter_password != enter_confirm_pwd:
            error_message = "Password and Confirm password are not matching!"
            return render(request, 'yd_webapp/register.html', locals())
        else:
            # Determine the entered email whether exists in database
            same_email = models.Patients.objects.filter(patient_email=enter_email)
            if same_email:
                error_message = "Email already exists in our system!"
                return render(request, 'yd_webapp/register.html', locals())

            # Everything is ok and then to create a new customer
            models.Patients.objects.create(
                patient_email=enter_email,
                patient_name=enter_name,
                patient_age=enter_age,
                patient_gender=enter_gender,
                patient_phone_num=enter_phone,
                address=enter_address,
                patient_psw=enter_password,
            )
            messages.success(request, 'Your account created successfully')

            return redirect('/yd_webapp/login/')

    return render(request, 'yd_webapp/register.html', locals())


# get接口
def show_questions(request):
    results = models.Record.objects.filter(answer_context='').order_by('-record_id')[0:3]
    list_all = []
    for result in results:
        collections = {}
        collections['records_id'] = result.record_id
        collections['username'] = result.patient_id.patient_name
        collections['question'] = result.question_context
        list_all.append(collections)
    return JsonResponse({'data':list_all,'code':200})


#存储问题的答案接口
@csrf_exempt
def save_answer(request):
    records_id = request.POST.get('records_id')
    answer = request.POST.get('answer')
    models.Record.objects.filter(record_id=records_id).update(answer_context=answer)
    return JsonResponse({'data': 'submit answer success!', 'code': 200})


#病人提问接口
# @csrf_exempt
def save_question_patient(request):
    if request.method == 'GET':
        return render(request, 'yd_webapp/questions.html')

    if request.method == 'POST':
        enter_email = request.POST.get('email')
        question_context = request.POST.get('question')
        print(enter_email)

        user_id = request.session.get('user_id')
        print(user_id)

        models.Record.objects.create(
            patient_id=models.Patients.objects.get(patient_id=user_id).patient_id,
            question_context=question_context,
        )

        print("question submit")
        return render(request, 'yd_webapp/questions.html', locals())

    # return JsonResponse({'data': 'submit questions success!', 'code': 200})


@csrf_exempt
def feedback(request):
    question = request.POST.get('question')
    feel = request.POST.get('feel')
    content = request.POST.get('content')
    models.Feedback.objects.create(question=question,feel=feel,content=content).save()
    return JsonResponse({'data': 'submit feedback success!', 'code': 200})


#页面
def show_questions_page(request):
    return render(request, 'yd_webapp/online_docter.html')


def show_questions_patient(request):
    return render(request, 'yd_webapp/questions.html')


def feedback_page(request):
    return render(request, 'yd_webapp/feedback.html')

