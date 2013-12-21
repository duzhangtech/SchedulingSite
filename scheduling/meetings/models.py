from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


class Meeting (models.Model):
	name = models.CharField(max_length=20)
	organizer = models.ForeignKey(User)
	pub_date = models.DateTimeField('date published')
	def __str__(self):
		return self.name
