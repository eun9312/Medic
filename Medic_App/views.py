from django.shortcuts import render, get_object_or_404
from django.db import transaction
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from Medic_App.forms import *

# Create your views here.

def home(request):
	currUser = request.user
	return render(request, 'index.html', {'user': currUser})

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
					email=form.cleaned_data['email'])
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

    new_profile = Profile(user=new_user, firstname=form.cleaned_data['firstname'], lastname=form.cleaned_data['lastname'], status=status)
    new_profile.save()

    return render(request, 'needs-confirmation.html', context)

def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    if not default_token_generator.check_token(user, token):
        raise Http404

    user.is_active = True
    user.save()
    return render(request, 'confirmed.html', {})
