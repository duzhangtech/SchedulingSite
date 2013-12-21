from django.shortcuts import render, get_object_or_404
from django.utils import timezone;
#from django.core.urlresolvers import reverse
from django.http import HttpResponse#, HttpResponseRedirect
from meetings.models import Meeting

def createMtn (request):
	return render(request, 'meetings/createMtn.html')

def create(request):
	new_meeting_object = Meeting(name=request.POST['meeting_name'], pub_date=timezone.now(), organizer=request.user)
	new_meeting_object.save()
#     return HttpResponseRedirect(reverse('meetings:meeting_creation_success', args=(new_meeting_object.id,)))
	return render(request, 'meetings/meeting_creation_success.html', {'name': new_meeting_object.name})
# def meeting_creation_success(request, meeting_id):
#     p = get_object_or_404(Meeting, pk=meeting_id);
#     return render(request, 'meetings/meeting_creation_success.html', {'name': p.name})

def organized(request):
	meeting_list = Meeting.objects.filter(organizer=request.user)
	return render(request, 'meetings/organized.html', {'list': meeting_list})