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
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp2 import views

urlpatterns = [
    path('', views.delivery_signup, name='delivery_signup'),
    path('delivery_index', views.delivery_index, name='delivery_index'),
    path('delivery_mywallet', views.delivery_mywallet, name='delivery_mywallet'),
    path('delivery_profile', views.delivery_profile, name='delivery_profile'),
    path('delivery_contact', views.delivery_contact, name='delivery_contact'),
    path('delivery_Withdrawal_funds', views.delivery_Withdrawal_funds, name='delivery_Withdrawal_funds'),
    path('delivery_profile_update', views.delivery_profile_update, name='delivery_profile_update'),
    path('delivery_login', views.delivery_login, name='delivery_login'),
    path('delivery_logout', views.delivery_logout, name='delivery_logout'),
    path('packages', views.packages, name='packages'),
    path('packages_details', views.packages_details, name='packages_details'),
    path('delivery_payments', views.delivery_payments, name='delivery_payments'),
    path('delivery_success', views.delivery_success, name='delivery_success'),
    path('change_password', views.change_password, name='change_password'),
    path('Withdrawal_funds/',views.Withdrawal_funds,name='Withdrawal_funds'), 
    path('accept', views.accept, name='accept'),
    path('reject', views.reject, name='reject'),
    path('finishride', views.finishride, name='finishride'),

]