"""
URL configuration for home_shifting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.usrls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('booking', views.booking, name='booking'),
    path('mybooking', views.mybooking, name='mybooking'),
    path('vehical', views.vehical, name='vehical'),
    path('service', views.service, name='service'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('change_pswd', views.change_pswd, name='change_pswd'),
    path('forget_pswd', views.forget_pswd, name='forget_pswd'),
    path('otp', views.otp, name='otp'),
    path('resetpass', views.resetpass, name='resetpass'),
    path('payments', views.payments, name='payments'),
    path('success', views.success, name='success'),
    path('utrack/ <int:pk>/',views.utrack, name="utrack"),
    path('cancel/ <int:pk>/',views.cancel, name="cancel"),
    
]