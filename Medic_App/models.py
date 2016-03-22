from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Status(models.Model):
	user = models.ForeignKey(User)
	status = models.CharField(max_length=30)

class Symptom(models.Model):
	name = models.CharField(max_length=30)

class Disease(models.Model):
	name = models.CharField(max_length=30)
	symptoms = models.ManyToManyField(Symptom, related_name="symptoms")
	description = models.CharField(max_length=500)

