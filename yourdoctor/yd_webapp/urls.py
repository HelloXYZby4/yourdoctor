from django.urls import path

from yd_webapp import views

app_name = 'yd_webapp'

urlpatterns = [

    path('', views.index, name='index'),
    path('timetable/',views.timetable,name='timetable')
]