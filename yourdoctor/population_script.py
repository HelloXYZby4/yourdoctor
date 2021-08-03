import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yourdoctor.settings')


import django
django.setup()


from yd_webapp.models import Patients, Doctors, Admins, Timetable, Record, Booking
import random


def populate():
    print("clean database")
    Patients.objects.all().delete()
    Doctors.objects.all().delete()
    Admins.objects.all().delete()
    Timetable.objects.all().delete()

    # patient number
    pn = 10
    # doctor number
    dn = 3

    # Patients
    for i in range(1, pn+1):
        Patients.objects.create(
            patient_id=i,
            patient_name='patient_name_'+str(i),
            patient_age=random.randint(0, 50),
            # patient_gender=random.randrange('female', 'male'),
            # patient_phone_num=random.randint(),
            patient_email='patient'+str(i)+'@gmail.com',
            patient_psw=str(i % 10)*6,
            address='address_'+str(i)
        )
    print("Patients Created! ")

    # Doctor
    doctor_name_list = ['Tim', 'John', 'Linda', 'Smith', 'Lia']
    for i in range(1, dn + 1):
        Doctors.objects.create(
            doctor_id=i,
            doctor_name=doctor_name_list[i],
            doctor_email=doctor_name_list[i] + '@gmail.com',
            doctor_psw=str(i % 10) * 6,
        )
    print("Doctors Created! ")

    # Admins
    Admins.objects.create(
        admin_id=1234,
        admin_email='system_admin@gmail.com',
        admin_psw=1234,
    )
    print("Admins Created! ")






if __name__ == '__main__':
    print('Starting population script...')
    populate()


