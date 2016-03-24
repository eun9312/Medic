from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
import random
import string

from Medic_App.forms import *

# Create your views here.

def home(request):
	return render(request, 'index.html', {})

def admin(request):
	if not request.user.is_authenticated() or not request.user.email == "medic.email.service@gmail.com":
    		raise Http404
	users = Status.objects.all()
	return render(request, 'admin.html', {'list': users})

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
    if not request.POST['status']:
	return render(request, 'register.html', context)
    if request.POST['status'] == 'doctor' and (len(request.FILES) != 2):
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

If you registered as medical doctor, it may take a few days until the administrator confirms your proof to practice medicine.
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

    if status == 'doctor':
	admin_email_body = """
Username: %s
First Name: %s
Last Name: %s
email: %s
confirmation link: http://%s%s
""" % (new_user.username, new_user.first_name, new_user.last_name, new_user.email,
       request.get_host(), reverse('confirm_doctor', args=(new_user.username, token)))
        admin_notify = EmailMessage(subject="New user doctor confirmation", body=admin_email_body,
			from_email="medic.email.service@gmail.com", to=["medic.email.service@gmail.com"])
	file1 = request.FILES['file1']
	file2 = request.FILES['file2']
	admin_notify.attach(file1.name, file1.read(), file1.content_type)
	admin_notify.attach(file2.name, file2.read(), file2.content_type)
	admin_notify.send()

    return render(request, 'needs-confirmation.html', context)

@transaction.atomic
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    if not default_token_generator.check_token(user, token):
        raise Http404

    user.is_active = True
    user.save()
    return render(request, 'confirmed.html', {})
    
@transaction.atomic
def confirm_doctor(request, username, token):
    if not request.user.is_authenticated() or not request.user.email == "medic.email.service@gmail.com":
    	raise Http404

    user = get_object_or_404(User, username=username)
    if not default_token_generator.check_token(user, token):
        raise Http404
    user_status = get_object_or_404(Status, user=user)


    user_status.status = 'doctor-confirmed'
    user_status.save()
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

