from django.db import forms
from yd_webapp.models import Patients, Doctors, Admins

from django.contrib.auth.models import User


class PatientsForm(forms.ModelForm):
    patient_id = forms.AutoField(primary_key=True)
    patient_name = forms.CharField(max_length=50, null=True)
    patient_email = forms.EmailField(null=True)
    patient_age = forms.IntegerField(null=True)
    patient_gender = forms.CharField(null=True)
    patient_phone_num = forms.CharField(max_length=20, null=True)
    patient_psw = forms.CharField(max_length=50, null=True)
    address = forms.CharField(max_length=200, null=True)

    class Meta:
        model = Patients
        fields = ('name', )


class DoctorsForm(forms.ModelForm):
    doctor_id = forms.AutoField(primary_key=True)
    doctor_name = forms.CharField(max_length=50, null=True)
    doctor_email = forms.EmailField(unique=True)
    doctor_psw = forms.CharField(max_length=50)


