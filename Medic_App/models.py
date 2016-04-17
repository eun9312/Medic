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
	symptoms = models.ManyToManyField(Symptom)
	commonness = models.CharField(max_length=1, choices=commonness_choices)
	added_by = models.ForeignKey(User)

type_choices = (
	("1", "medic chat"),
	("2", "patients chat"),
)

class ChatRoom(models.Model):
	name = models.CharField(max_length=100)
	participants = models.ManyToManyField(User)
	type = models.CharField(max_length=20, choices=type_choices)

class Message(models.Model):
	sent = models.ForeignKey(User)
	room = models.ForeignKey(ChatRoom)
	content = models.CharField(max_length=500)
