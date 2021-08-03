from django.db import models

# Create your models here.


class Patients(models.Model):
    patient_id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=50, null=True)
    # patient_last_name = models.CharField(max_length=50, null=True)
    patient_email = models.EmailField(null=True)
    patient_age = models.IntegerField(null=True)
    patient_gender = models.CharField(null=True)
    patient_phone_num = models.CharField(max_length=20, null=True)
    patient_psw = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=200, null=True)




