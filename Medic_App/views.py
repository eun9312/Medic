from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import random
import string

from Medic_App.forms import *

# Create your views here.

def home(request):
	return render(request, 'index.html', {})

def info(request):
	return render(request, 'info.html', {})

def checkup(request):
	return render(request, 'check-up.html', {})

@login_required
def medicchat(request):
	return render(request, 'medic_chat.html', {})

@login_required
def patientschat(request):
	return render(request, 'patients_chat.html', {})

@transaction.atomic
def register(request):
    context = {}

    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'register.html', context)

    form = RegistrationForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'register.html', context)

    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password1'],
					email=form.cleaned_data['email'],
					first_name=form.cleaned_data['firstname'],
					last_name=form.cleaned_data['lastname'])
    new_user.is_active = False
    new_user.save()

    token = default_token_generator.make_token(new_user)

    email_body = """
Please click the link below to verify your email address and complete the registration:
http://%s%s
""" % (request.get_host(), 
       reverse('confirm', args=(new_user.username, token)))

    send_mail(subject="Verify your email address",
              message= email_body,
              from_email="medic.email.service@gmail.com",
              recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']

    if (request.POST['status'] == 'doctor') :
	    status = 'doctor'
    else:
	    status = 'patient'

    new_status = Status(user=new_user, status=status)
    new_status.save()

    return render(request, 'needs-confirmation.html', context)

@transaction.atomic
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    if not default_token_generator.check_token(user, token):
        raise Http404

    user.is_active = True
    user.save()
    return render(request, 'confirmed.html', {})

def find_username(request):
    context = {}

    if request.method == 'GET':
        return render(request, 'find_username.html', context)

    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    email = request.POST['email']

    try:
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
	return render(request, 'find_username.html', {'error': 'No user matches the information.'})
    if (user.first_name != firstname or user.last_name != lastname) :
        return render(request, 'find_username.html', {'error': 'No user matches the information.'})

    email_body = """
Your username is
%s
""" % (user.username)

    send_mail(subject="Your username",
              message= email_body,
              from_email="medic.email.service@gmail.com",
              recipient_list=[email])

    context['email'] = email

    return render(request, 'needs-confirmation.html', context)

@transaction.atomic
def find_password(request):
    context = {}

    if request.method == 'GET':
        return render(request, 'find_password.html', context)

    username = request.POST['username']
    email = request.POST['email']

    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
	return render(request, 'find_password.html', {'error': 'No user matches the information.'})
    if (user.email != email) :
        return render(request, 'find_password.html', {'error': 'No user matches the information.'})

    new_password = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))

    email_body = """
Your new password is
%s
""" % (new_password)

    send_mail(subject="Your password",
              message= email_body,
              from_email="medic.email.service@gmail.com",
              recipient_list=[email])

    user.set_password(new_password)
    user.save()
    context['email'] = email

    return render(request, 'needs-confirmation.html', context)

