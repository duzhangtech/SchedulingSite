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
	pub_date = models.DateTimeField('date published')
	def __str__(self):
		return self.name