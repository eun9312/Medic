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
import json

from Medic_App.forms import *

# Create your views here.

def home(request):
	return render(request, 'index.html', {})

def admin(request):
	if not request.user.is_authenticated() or not request.user.email == "medic.email.service@gmail.com":
    		raise Http404
	users = Status.objects.all()
	return render(request, 'admin.html', {'list': users})

def admin_symptom(request):
	if not request.user.is_authenticated() or not request.user.email == "medic.email.service@gmail.com":
    		raise Http404
	type = SymptomType.objects.all()
	detail = Symptom.objects.all()
	return render(request, 'admin_symptom.html', {'type': type, 'detail': detail})

def info(request):
	return render(request, 'info.html', {})

def checkup(request):
    symptomTypeList = SymptomType.objects.order_by('name')
    return render(request, 'check-up.html', {'symptomTypeList':symptomTypeList})

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
	    status = 'need-confirmation'
    else:
	    status = 'patient'

    new_status = Status(user=new_user, status=status)
    new_status.save()

    if status == 'need-confirmation':
	admin_email_body = """
Username: %s
First Name: %s
Last Name: %s
email: %s
confirmation link: http://%s%s
declination link: http://%s%s
""" % (new_user.username, new_user.first_name, new_user.last_name, new_user.email,
       request.get_host(), reverse('confirm_doctor', kwargs={'username':new_user.username}),
       request.get_host(), reverse('confirm_patient', kwargs={'username':new_user.username}))
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
def confirm_doctor(request, username):
    if not request.user.is_authenticated() or not request.user.email == "medic.email.service@gmail.com":
    	raise Http404

    user = get_object_or_404(User, username=username)
    user_status = get_object_or_404(Status, user=user)

    user_status.status = 'doctor'
    user_status.save()
    return redirect(reverse('admin'))

@transaction.atomic
def confirm_patient(request, username):
    if not request.user.is_authenticated() or not request.user.email == "medic.email.service@gmail.com":
    	raise Http404

    user = get_object_or_404(User, username=username)
    user_status = get_object_or_404(Status, user=user)

    user_status.status = 'patient'
    user_status.save()
    return redirect(reverse('admin'))

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

def add_symptom(request):
    if not request.user.is_authenticated():
        return render(request, 'not_doc.html', {})
    user_status = get_object_or_404(Status, user=request.user)
    if user_status.status == "patient":
        return render(request, 'not_doc.html', {})
    if user_status.status == "need-confirmation":
        return render(request, 'not_confirmed_doc.html', {})
    if user_status.status != "doctor":
	return Http404

    symptomTypeList = SymptomType.objects.order_by('name')
    return render(request, 'add_symptom.html', {'symptomTypeList': symptomTypeList})

@transaction.atomic
def add_symptom_type(request):
    symptomTypeList = SymptomType.objects.all()
    if not request.POST['symptom_type']:
        return render(request, 'add_symptom.html', {'errortype': 'Please enter a valid symptom type.',
		'symptomTypeList': symptomTypeList})

    try:
        type = SymptomType.objects.get(name=request.POST['symptom_type'])
	return render(request, 'add_symptom.html', {'errortype': 'The symptom type you entered already exists in the database.',
		'symptomTypeList': symptomTypeList})
    except ObjectDoesNotExist:
	type = SymptomType(name=request.POST['symptom_type'], added_by=request.user)
	type.save()
	return render(request, 'updated.html', {})

@transaction.atomic
def add_symptom_detail(request):
    symptomTypeList = SymptomType.objects.all()
    if not request.POST['symptom_type'] or request.POST['symptom_type'] == '':
        return render(request, 'add_symptom.html', {'errordetail': 'Please select a symptom type.',
		'symptomTypeList': symptomTypeList})
    if not request.POST['symptom_detail']:
        return render(request, 'add_symptom.html', {'errordetail': 'Please enter a valid symptom detail.',
		'symptomTypeList': symptomTypeList})

    try:
        detail = Symptom.objects.get(name=request.POST['symptom_detail'])
	if (detail.symptomType.name == request.POST['symptom_type']):
            return render(request, 'add_symptom.html', {'errordetail': 'The symptom detail you entered already exists in the database.',
		'symptomTypeList': symptomTypeList})
	else: raise ObjectDoesNotExist()
    except ObjectDoesNotExist:
	type = get_object_or_404(SymptomType, name=request.POST['symptom_type'])
	detail = Symptom(name=request.POST['symptom_detail'], symptomType=type, added_by=request.user)
	detail.save()
	return render(request, 'updated.html', {})
    return render(request, 'updated.html', {})

def add_disease(request):
    return render(request, 'add_disease.html', {})

@transaction.atomic
def delete_symptom_type(request, name):
    if not request.user.is_authenticated() or not request.user.email == "medic.email.service@gmail.com":
        raise Http404
    type = get_object_or_404(SymptomType, name=name)
    type.delete()
    return redirect(reverse('admin_symptom'))


@transaction.atomic
def delete_symptom_detail(request):
    if not request.user.is_authenticated() or not request.user.email == "medic.email.service@gmail.com":
        raise Http404
    detail = get_object_or_404(Symptom, name=name)
    detail.delete()
    return redirect(reverse('admin_symptom'))

def parseDetails(symptom_list):
    list = []
    for s in symptom_list:
        data={}
	data['name'] = s.name
	data['type'] = s.symptomType.name
        list.append(data)
    return list

def get_detail_list(request):
    if not 'type' in request.POST or not request.POST['type']:
        return
    type = get_object_or_404(SymptomType, name=request.POST['type'])
    symptom_list = Symptom.objects.filter(symptomType=type).order_by('name')
    return HttpResponse(json.dumps(parseDetails(symptom_list)), content_type='application/json')

