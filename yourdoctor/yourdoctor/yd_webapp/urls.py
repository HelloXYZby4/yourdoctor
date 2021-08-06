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

    path('show_questions/', views.show_questions, name='show_questions'),
    path('save_answer/', views.save_answer, name='save_answer'),
    # path('sqp/', views.show_questions_patient, name='show_questions_patient'),
    # path('save_question_patient/', views.ask_question_patient, name='show_questions_patient'),
    path('feedback/', views.feedback, name='feedback'),
    path('feedback_page/', views.feedback_page, name='feedback'),
    path('message/', views.save_question_patient, name='message'),
    # path('onlinedoctor/',views.show_questions_page, name='onlinedoctor')
    path('onlinedoctor/',views.answer_question, name='onlinedoctor')


]
