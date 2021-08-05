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
    path('index/', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('doclogin/', views.doc_login, name='doclogin'),
]