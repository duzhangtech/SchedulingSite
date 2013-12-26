#Stdlib imports
import string
import random
from datetime import date, timedelta

from django.core.context_processors import csrf
from django.shortcuts import render, get_object_or_404, render_to_response
from django.utils import timezone
from django.contrib.auth.models import User
#from django.core.urlresolvers import reverse
from django.http import HttpResponse#, HttpResponseRedirect
from meetings.models import Meeting
# Define the date row
def giveDate(num):
    if num == 0: return 'Sunday'
    if num == 1: return 'Monday'
    if num == 2: return 'Tuesday'
    if num == 3: return 'Wednesday'
    if num == 4: return 'Thursday'
    if num == 5: return 'Friday'
    if num == 6: return 'Saturday'
today_date = date.today().weekday()
global datesForData #Define the data processing needs
datesForData = [date.today(), \
                date.today()+timedelta(days = 1),\
                date.today()+timedelta(days = 2),\
                date.today()+timedelta(days = 3),\
                date.today()+timedelta(days = 4),\
                date.today()+timedelta(days = 5),\
                date.today()+timedelta(days = 6)]
global display
display = [giveDate(today_date),\
    giveDate((today_date+1)%7),\
    giveDate((today_date+2)%7),\
    giveDate((today_date+3)%7),\
    giveDate((today_date+4)%7),\
    giveDate((today_date+5)%7),\
    giveDate((today_date+6)%7)]
#Define the clock col
clock = []
for num in range(0,11):
    k = (num*2 + 5);
    if k > 12:
        clock.append(str(k%12)+"pm");
    elif k < 12 :
        clock.append(str(k%12)+"am");
#data processing
def singleProcessor(string):
    if string[0] == '0':
        if string[2] == '3':
            k = 1
        else: 
            k = 0
        k = k + 2*(int(string[1]) - 5)
    else:
        if string[2] == '3':
            k = 1
        else: 
            k = 0
        k = k + 2*(int(string[0:2]) - 5)

    return k

def processor(proposed):
    tempStorage = []
    num = len(proposed)/16
    today = str(date.today())
    today = today[5:] + "-"+today[0:4]
    for i in range(0,num):
        p = singleProcessor(proposed[16*i:16*(i+1)-12])
        n = singleProcessor(proposed[16*(i+1)-12:16*(i+1)-8])
        tempStorage.append(p)
        tempStorage.append(n)
        w = 1 + int(proposed[16*i+10:16*i+12]) - int(today[3:5])
        tempStorage.append(w)
    
    return tempStorage

def descriptionProcessor(proposed):
    tempStorage = []
    num = len(proposed)/16
    for i in range(0,num):
        tempStorage.append(proposed[0+i*16:2+i*16]+":"+proposed[2+i*16:4+i*16])
        tempStorage.append('-')
        tempStorage.append(proposed[4+i*16:6+i*16]+":"+proposed[6+i*16:8+i*16])
    return tempStorage
#6-digit random id generator
def index_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

a ={}
a['clock'] = clock
a['date'] = display
a['datesForData'] = datesForData

def createMtn (request):
    a = {}
    a.update(csrf(request))
    a['user'] = request.user
    a['clock'] = clock
    a['date'] = display
    a['datesForData'] = datesForData
    a['list_organized'] = request.user.meetings_organized.all()
    a['list_invited'] = request.user.meetings_invited.all()
    return render_to_response("meetings/createMtn.html", a)

def create(request):
    new_meeting_object = Meeting(meeting_id=index_generator(), description=request.POST['meeting_description'] ,proposed = request.POST['proposed'], name=request.POST['meeting_name'], pub_date=timezone.now(), organizer=request.user)
    new_meeting_object.save()
    for i in range(1, 6):
		form_in = request.POST['invited_' + str(i)]
		if form_in != '':
			u = User.objects.get(username=form_in)
			new_meeting_object.invited.add(u)
			new_meeting_object.save()
    b = a
    b['user'] = request.user
    b['list_organized'] = request.user.meetings_organized.all()
    b['list_invited'] = request.user.meetings_invited.all()  
    b['name'] = new_meeting_object.name
    return render_to_response('meetings/meeting_creation_success.html', b)

def MtnOrganized(request, meeting_id):
    meeting = Meeting.objects.get(meeting_id = meeting_id)
    b = a
    b['meeting'] = meeting
    b['user'] = request.user
    b['list_organized'] = request.user.meetings_organized.all()
    b['list_invited'] = request.user.meetings_invited.all()
    b['data'] = processor(meeting.proposed)     
    return render_to_response('meetings/meeting_organized.html', b)

def MtnInvited(request, meeting_id):
    meeting = Meeting.objects.get(meeting_id = meeting_id)
    b = a
    b['meeting'] = meeting
    b['user'] = request.user
    b['list_organized'] = request.user.meetings_organized.all()
    b['list_invited'] = request.user.meetings_invited.all()     
    b['data'] = processor(meeting.proposed)  
    b['length'] = len(b['data'])/3
    b['specificTimeDispaly'] = descriptionProcessor(meeting.proposed)
    return render_to_response('meetings/meeting_invited.html', b)