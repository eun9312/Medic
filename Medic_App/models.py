from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

status_choices = (
	("0", "need-confirmation"),
	("1", "patient"),
	("2", "doctor"),
)

class Status(models.Model):
	user = models.ForeignKey(User)
	status = models.CharField(max_length=30, choices=status_choices)

class SymptomType(models.Model):
	name = models.CharField(max_length=50)
	added_by = models.ForeignKey(User)

class Symptom(models.Model):
	name = models.CharField(max_length=100)
	symptomType = models.ForeignKey(SymptomType)
	added_by = models.ForeignKey(User)

commonness_choices = (
	("1", "very uncommon"),
	("2", "uncommon"),
	("3", "common"),
	("4", "very common"),
)

class Disease(models.Model):
	name = models.CharField(max_length=50)
	symptoms = models.ManyToManyField(Symptom, related_name="symptoms")
	commonness = models.CharField(max_length=30, choices=commonness_choices)
	added_by = models.ForeignKey(User)

