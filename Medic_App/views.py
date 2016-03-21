from django.shortcuts import render

# Create your views here.

def home(request):
	return render(request, 'index.html', {})

def info(request):
	return render(request, 'info.html', {})

def checkup(request):
	return render(request, 'check-up.html', {})

def medicchat(request):
	return render(request, 'medic_chat.html', {})

def patientschat(request):
	return render(request, 'patients_chat.html', {})
