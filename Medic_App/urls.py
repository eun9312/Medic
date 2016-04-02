"""Medic_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from Medic_App import views as medic_views
from django.contrib.auth import views as auth_views
from Medic_App import forms

urlpatterns = [
    url(r'^$', medic_views.home, name='home'),
    url(r'^admin$', medic_views.admin, name='admin'),
    url(r'^admin/symptom$', medic_views.admin_symptom, name='admin_symptom'),
    url(r'^info$', medic_views.info, name='info'),
    url(r'^check-up$', medic_views.checkup, name='check-up'),
    url(r'^medic_chat$', medic_views.medicchat, name='medic_chat'),
    url(r'^patients_chat$', medic_views.patientschat, name='patients_chat'),
    url(r'^login$', auth_views.login, {'template_name':'login.html', 'authentication_form': forms.LoginForm}, name='login'),
    url(r'^logout$', auth_views.logout, {'next_page': '/medic'}, name='logout'),
    url(r'^register$', medic_views.register, name='register'),
    url(r'^confirm-registration/(?P<username>\w+)/(?P<token>[a-z0-9\-]+)$',
        medic_views.confirm_registration, name='confirm'),
    url(r'^confirm-doctor/(?P<username>\w+)$',
        medic_views.confirm_doctor, name='confirm_doctor'),
    url(r'^confirm-patient/(?P<username>\w+)$',
        medic_views.confirm_patient, name='confirm_patient'),
    url(r'^find_username$', medic_views.find_username, name='find_username'),
    url(r'^find_password$', medic_views.find_password, name='find_password'),
    url(r'^add_symptom$', medic_views.add_symptom, name='add_symptom'),
    url(r'^add_disease$', medic_views.add_disease, name='add_disease'),
    url(r'^add_symptom_type$', medic_views.add_symptom_type, name='add_symptom_type'),
    url(r'^add_symptom_detail$', medic_views.add_symptom_detail, name='add_symptom_detail'),
    url(r'^delete_symptom_type/(?P<name>[\w\s]+)$', medic_views.delete_symptom_type, name='delete_symptom_type'),
    url(r'^delete_symptom_detail/(?P<name>[\w\s]+)$', medic_views.delete_symptom_detail, name='delete_symptom_detail'),
]
