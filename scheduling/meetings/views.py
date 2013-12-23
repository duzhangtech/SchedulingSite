from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User
#from django.core.urlresolvers import reverse
from django.http import HttpResponse#, HttpResponseRedirect
from meetings.models import Meeting

def createMtn (request):
	return render(request, 'meetings/createMtn.html')

def create(request):
	new_meeting_object = Meeting(name=request.POST['meeting_name'], pub_date=timezone.now(), organizer=request.user)
	new_meeting_object.save()
	for i in range(1, 6):
		form_in = request.POST['invited_' + str(i)]
		if form_in != '':
			u = User.objects.get(username=form_in)
			new_meeting_object.invited.add(u)
			new_meeting_object.save()
	return render(request, 'meetings/meeting_creation_success.html', {'name': new_meeting_object.name})

def organized(request):
	# meeting_list = Meeting.objects.filter(organizer=request.user)
	meeting_list = request.user.meetings_organized.all()
	return render(request, 'meetings/organized.html', {'list': meeting_list})

def invited(request):
	invited_list = request.user.meetings_invited.all()
	return render(request, 'meetings/invited.html', {'list':invited_list})