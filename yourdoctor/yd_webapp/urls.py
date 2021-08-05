from django.urls import path

from yd_webapp import views

app_name = 'yd_webapp'

urlpatterns = [

    path('', views.index, name='index'),
    path('timetable/',views.timetable,name='timetable'),
    path('patient/',views.useraccount,name='user'),
    path('edittime/',views.edittime,name='edittime'),
    path('booking/', views.booking, name='booking'),
    path('doctor/', views.doctoraccount, name='doctor'),
]