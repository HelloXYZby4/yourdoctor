from django.shortcuts import render, redirect
from django.http import HttpResponse
from yd_webapp import models
from django.contrib import messages

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
def register_submit(request):
    if request.method == 'POST':
        enter_email = request.POST.get('email', '')
        enter_name = request.POST.get('name', '')
        enter_age = request.POST.get('age', '')
        enter_gender = request.POST.get('gender', '')
        enter_phone = request.POST.get('phone', '')
        enter_address = request.POST.get('address', '')
        enter_password = request.POST.get('password', '')
        enter_confirm_pwd = request.POST.get('confirm_pwd', '')

        # Determine whether any received data is empty
        if not enter_email.strip():
            error_message = "Email can not be empty"
            return render(request, 'register.html', locals())
        elif not enter_name.strip():
            error_message = "Name can not be empty"
            return render(request, 'register.html', locals())
        elif not enter_age.strip():
            error_message = "Age can not be empty"
            return render(request, 'register.html', locals())
        elif not enter_gender.strip():
            error_message = "Gender can not be empty"
            return render(request, 'register.html', locals())
        elif not enter_phone.strip():
            error_message = "Phone number can not be empty"
            return render(request, 'register.html', locals())
        elif not enter_address.strip():
            error_message = "Address can not be empty"
            return render(request, 'register.html', locals())
        elif not enter_password.strip():
            error_message = "Password can not be empty"
            return render(request, 'register.html', locals())
        elif not enter_confirm_pwd.strip():
            error_message = "Confirm password can not be empty"
            return render(request, 'register.html', locals())

        # Determine email format and password and confirm_password whether same
        if not validate_email(enter_email):
            error_message = "Email format is wrong!"
            return render(request, 'register.html', locals())
        elif len(enter_password) < 7:
            error_message = "Password length must not be less than 7 characters!"
        elif enter_password != enter_confirm_pwd:
            error_message = "Password and Confirm password are not matching!"
            return render(request, 'register.html', locals())
        else:
            # Determine the entered email whether exists in database
            same_email = models.Patients.objects.filter(patient_email=enter_email)
            if same_email:
                error_message = "Email already exists in our system!"
                return render(request, 'register.html', locals())

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

            return redirect('/longin/')
    return render(request, 'register.html')


# link to the login page
def login(request):
    return render(request, 'login.html')


# login submit
def login_submit(request):
    if request.method == 'POST':
        print("the POST method from Login Page")

        # Determine whether the parameters are passed to back_end
        enter_email = request.POST.get('email', '')
        enter_password = request.POST.get('password', '')
        enter_role = request.POST.get('role', '')
        print('email:', enter_email, "\npassword:", enter_password, "\nrole:", enter_role)

        # user role is Patient
        if enter_role == 'Patient':
            try:
                user = models.Patients.objects.get(patient_email=enter_email)
                if enter_password == user.patient_psw:
                    # request.session['is_login'] = True
                    # request.session['user_id'] = user.customer_id
                    # request.session['user_first_name'] = user.customer_first_name
                    # request.session['user_last_name'] = user.customer_last_name
                    # request.session['user_email'] = user.customer_email
                    # request.session['user_phone'] = user.customer_phone_num
                    # request.session['user_balance'] = user.balance
                    return redirect('/homepage/')
                else:
                    error_message = "Email and Password are not matching!"
            except:
                error_message = "Email is not exist in our system"

        # user role is doctor
        elif enter_role == 'Doctor':
            print('doctor log in')
            try:
                user = models.Doctors.objects.get(doctor_email=enter_email)
                if enter_password == user.doctor_email:
                    request.session['is_login'] = True
                    print('ok*********')
                    return redirect('/doctor')
                else:
                    error_message = "Email and Password are not matching!"
            except Exception as e:
                error_message = e

        # user role is manager
        elif enter_role == 'Admin':
            try:
                user = models.Admins.objects.get(admin_email=enter_email)
                # if hash_code(enter_password) == user.manager_psw:
                if enter_password == user.manager_psw:
                    request.session['is_login'] = True
                    return redirect('/admins/')
                else:
                    error_message = "Email and Password are not matching!"
            except Exception as e:
                error_message = e
    return render(request, 'login.html')


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



