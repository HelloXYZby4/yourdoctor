from django.test import TestCase
from yd_webapp.models import Patients,Doctors
from django.urls import resolve
from django.http import HttpRequest
from population_script import populate
from yd_webapp.views import index
# Create your tests here.


class Patient_Test(TestCase):

    def test_create(Self):

        Patients.objects.create(
                patient_email="2500338F@student.gla.ac.uk",
                patient_name="Yupeng Fu",
                patient_age="24",
                patient_gender="male",
                patient_phone_num="123123123",
                address="Glasgow",
                patient_psw="123123",
            )

    def test_get(self):

        Patients.objects.create(
                patient_email="2500338F@student.gla.ac.uk",
                patient_name="Yupeng Fu",
                patient_age="24",
                patient_gender="male",
                patient_phone_num="123123123",
                address="Glasgow",
                patient_psw="123123",
            )
        p = Patients.objects.get(patient_email="2500338F@student.gla.ac.uk")

        self.assertEqual(p.patient_age,24)
        self.assertEqual(p.address,"Glasgow")


class Doctor_Test(TestCase):

    def test_create(Self):
        Doctors.objects.create(
                
                doctor_email="2500338F@student.gla.ac.uk",
                doctor_psw="123",
                doctor_name="Yupeng Fu",
            )

    def test_get(self):
        Doctors.objects.create(
                
                doctor_email="2500338F@student.gla.ac.uk",
                doctor_psw="123",
                doctor_name="Yupeng Fu",
                
            )
        p =Doctors.objects.get(doctor_email="2500338F@student.gla.ac.uk")
        self.assertEqual(p.doctor_name,"Yupeng Fu")


class PopulationScriptTest(TestCase):

    def setUp(self):
        populate()
    
    def test_page_objects_have_views(self):

        Patient = Patients.objects.get(patient_id=5)
        self.assertEqual(Patient.patient_name,'patient_name_'+str(5))


class HomePageTest(TestCase):

    def test_root_url_to_home_page(self):
        found = resolve('/') 
        self.assertEqual(found.func, index) 
