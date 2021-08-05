from django.urls import path

from yd_webapp import views


app_name = "yd_webapp"
urlpatterns = [

    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
]