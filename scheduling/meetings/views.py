#Stdlib imports
import re
import string
import random
from time import mktime, strptime
from datetime import datetime, date, timedelta
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.utils import timezone
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from meetings.models import Meeting, Respond
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
from time import mktime, strptime
from datetime import datetime, date

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
def dateProcessor(timestring):
    #conver string to datetime object
    a = strptime(timestring, "%m%d%Y")
    a = datetime.fromtimestamp(mktime(a))
    a = a - datetime.today()
    a = a.days
    return a + 2
def processor(proposed): #takeproposed raw data, return the dates in format
    tempStorage = []
    num = len(proposed)/16
    for i in range(0,num):
        p = singleProcessor(proposed[16*i:16*(i+1)-12])
        n = singleProcessor(proposed[16*(i+1)-12:16*(i+1)-8])
        w = dateProcessor(proposed[16*i+8:16*i+16]) 
        tempStorage.append(p)
        tempStorage.append(n)
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
#organizer page's display info processor
def organizerPageProcessor(proposed):
    tempStorage = []
    num = len(proposed)/16
    for i in range(0,num):
        tempStorage.append(proposed[16*i+8:16*i+10]+'/'+proposed[16*i+10:16*i+12])
        tempStorage.append(proposed[0+i*16:2+i*16]+":"+proposed[2+i*16:4+i*16]+'-'+proposed[4+i*16:6+i*16]+":"+proposed[6+i*16:8+i*16])
    tempStorage = [x+y for x,y in zip(tempStorage[0::2], tempStorage[1::2])]
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
    # the raw value for result
    length = len(request.POST['proposed'])/16
    new_meeting_object = Meeting(result = ''.join(map(str, [k for k in range(0,length)])), meeting_id=index_generator(), description=request.POST['meeting_description'] ,proposed = request.POST['proposed'], name=request.POST['meeting_name'], pub_date=timezone.now(), organizer=request.user)
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
    b = {}
    b.update(csrf(request))
    b['clock'] = clock
    b['date'] = display
    b['datesForData'] = datesForData
    b['meeting'] = meeting
    b['user'] = request.user
    b['list_organized'] = request.user.meetings_organized.all()
    b['list_invited'] = request.user.meetings_invited.all()     
    b['data'] = processor(meeting.proposed)  
    b['length'] = len(b['data'])/3
    length = len(b['data'])/3
    b['specificTimeDispaly'] = descriptionProcessor(meeting.proposed)
    b['infoOnTop'] = organizerPageProcessor(meeting.proposed)
    b['amountOfAvail'] = [x for x in range(0, b['length'])]
#processing for responses--------------
    k = '<td>&#32</td>'
#first row
    for response in meeting.responses.all():
        k = k + '<td>'+response.responder.username+'</td>'
    k = '<tr>'+k+'</tr>'
#other rows
    counter = 0 
    for num in organizerPageProcessor(meeting.proposed):
        k = k + '<tr>'
        k = k + '<td>'+ num +'</td>'
        for x in range(0, meeting.responses.count()):
            thisResponder = Respond.objects.filter(meeting = meeting)[x]
            if str(counter) in thisResponder.choice:
                k = k + '<td class = "availChoice">&#10004</td>'
            else:
                k = k + '<td class = "unavailChoice">&#215</td>'
        counter = counter + 1
        k = k + '</tr>'
    k= '<table>' + k +'</table>'
    b['table'] = k
    return render_to_response('meetings/meeting_organized.html', b)

def delete(request, meeting_id):
    meeting = Meeting.objects.get(meeting_id = meeting_id,)
    meeting.delete()
    return HttpResponseRedirect('/loggedin/')

def MtnInvited(request, meeting_id):
    meeting = Meeting.objects.get(meeting_id = meeting_id)
    b = {}
    b.update(csrf(request))
    b['clock'] = clock
    b['date'] = display
    b['datesForData'] = datesForData
    b['meeting'] = meeting
    b['user'] = request.user
    b['list_organized'] = request.user.meetings_organized.all()
    b['list_invited'] = request.user.meetings_invited.all()     
    b['data'] = processor(meeting.proposed)  
    b['length'] = len(b['data'])/3
    b['specificTimeDispaly'] = descriptionProcessor(meeting.proposed)
    b['amountOfAvail'] = [x for x in range(0, b['length'])]
    try:
        c = request.user.response.get(meeting = meeting,)
        return HttpResponseRedirect('/loggedin/invited/%s/responded' % meeting.meeting_id)
    except ObjectDoesNotExist:
        return render_to_response('meetings/meeting_invited.html', b)

def respond(request, meeting_id):
    meeting = Meeting.objects.get(meeting_id = meeting_id)
    b = {}
    b.update(csrf(request))
    b['clock'] = clock
    b['date'] = display
    b['datesForData'] = datesForData
    b['meeting'] = meeting
    b['user'] = request.user
    b['list_organized'] = request.user.meetings_organized.all()
    b['list_invited'] = request.user.meetings_invited.all()     
    b['data'] = processor(meeting.proposed)  
    b['length'] = len(b['data'])/3
    b['specificTimeDispaly'] = descriptionProcessor(meeting.proposed)
    b['amountOfAvail'] = [x for x in range(0, b['length'])]
    b['responded'] = "You have selected"
    choice = "".join(request.POST.getlist("selectedTime"))
    choice = str(filter(lambda x: x.isdigit(), choice))

    try :
        c = request.user.response.get(meeting = meeting)
        choice = "".join(request.POST.getlist("selectedTime"))
        choice = str(filter(lambda x: x.isdigit(), choice))
        c.choice = choice
        c.save()
    except ObjectDoesNotExist:
# result processing
        d = meeting.respond_set.create(responder = request.user, choice = choice, pub_date=timezone.now())
# result processing
    newResult = str(meeting.result)
    for letter in newResult:
        if letter not in choice:
            temp = newResult.replace(letter, '')
            newResult = temp
    meeting.result = newResult
    meeting.save()

    return HttpResponseRedirect('/loggedin/invited/%s/responded' % meeting.meeting_id)
def responded(request, meeting_id):
    meeting = Meeting.objects.get(meeting_id = meeting_id)
    b = {}
    b.update(csrf(request))
    b['clock'] = clock
    b['date'] = display
    b['datesForData'] = datesForData
    b['meeting'] = meeting
    b['user'] = request.user
    b['list_organized'] = request.user.meetings_organized.all()
    b['list_invited'] = request.user.meetings_invited.all()     
    b['data'] = processor(meeting.proposed)  
    b['length'] = len(b['data'])/3
    b['specificTimeDispaly'] = descriptionProcessor(meeting.proposed)
    b['amountOfAvail'] = [x for x in range(0, b['length'])]
    b['responded'] = "You have selected, just submit another form to update your results"
#update the new mtn
# result processing
    return render_to_response('meetings/meeting_invited.html', b)