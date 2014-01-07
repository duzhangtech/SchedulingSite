from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


class Meeting (models.Model):
	name = models.CharField(max_length = 20)
	description = models.CharField(max_length = 100)
	proposed = models.CharField(max_length = 200)
	organizer = models.ForeignKey(User, related_name='meetings_organized')
	invited = models.ManyToManyField(User, related_name='meetings_invited')
	meeting_id = models.CharField(max_length = 7)
	result = models.CharField(max_length = 20)
	pub_date = models.DateTimeField('date published')
	visibility = models.BooleanField(default = False)
	def __str__(self):
		return self.name

class Respond(models.Model):
	choice = models.CharField(max_length=50 , blank = True)
	preference = models.CharField(max_length=50, blank = True)
	pub_date = models.DateTimeField('date published')
	responder = models.ForeignKey(User, related_name='response')
	responder_unregistered = models.CharField(max_length=10, )
	meeting = models.ForeignKey(Meeting,related_name='responses')
	def __str__(self):
		return self.choice