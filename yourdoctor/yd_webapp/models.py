from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.


class Patients(models.Model):
    patient_id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=50, null=True)
    patient_email = models.EmailField(null=True)
    patient_age = models.IntegerField(null=True)
    patient_gender = models.CharField(max_length=5, null=True)
    patient_phone_num = models.CharField(max_length=20, null=True)
    patient_psw = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=200, null=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.patient_name)
        super(Patients, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Patients'

    def __str__(self):
        return str(self.patient_id)


class Doctors(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    doctor_name = models.CharField(max_length=50, null=True)
    doctor_email = models.EmailField(unique=True)
    doctor_psw = models.CharField(max_length=50)

    def __str__(self):
        return str(self.doctor_id)


class Admins(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_email = models.EmailField(unique=True)
    admin_psw = models.CharField(max_length=50)

    def __str__(self):
        return (self.admin_id)


# contains the doctors' available time so that the doctors can choose
# t_id: the unique id of all the available time of each doctor
# time_id: from Mon. to Fri.
class Timetable(models.Model):
    t_id = models.AutoField(primary_key=True, default=0)
    doctor_id = models.ForeignKey('Doctors', on_delete=models.CASCADE, null=True)
    time_choices = (
        (1, u'Mon.'),
        (2, u'Tue.'),
        (3, u'Wed.'),
        (4, u'Thu.'),
        (5, u'Fri.'),
    )
    time_id = models.IntegerField(choices=time_choices, null=True)
    status_choices = (
        (0, u'available'),
        (1, u'not available')
    )
    status = models.IntegerField(choices=status_choices, default=0)

    def __str__(self):
        return self.t_id


# contains patients' questions and the answers from the doctor
class Record(models.Model):
    record_id = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey('Patients', on_delete=models.CASCADE)
    doctor_id = models.ForeignKey('Doctors', on_delete=models.CASCADE)
    question_context = models.CharField(max_length=500, default='')
    answer_context = models.CharField(max_length=500, default='')


# contains the booking details about the patients
class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey('Patients', on_delete=models.CASCADE)
    t_id = models.ForeignKey('Timetable', null=True, on_delete=models.CASCADE)






from django.contrib import admin

admin.site.register(Patients)
admin.site.register(Doctors)
admin.site.register(Admins)


