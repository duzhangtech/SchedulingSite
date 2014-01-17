# -*- coding: utf-8 -*- 
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
#core
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.core.context_processors import csrf
from forms import MyRegistrationForm
from django.contrib.auth.decorators import login_required
#models
from meetings.models import Meeting, Respond

def index(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect("/loggedin")
	else:
		c = {}
		c.update(csrf(request))
		form = MyRegistrationForm()
		form.fields['password1'].label = "密码"
		form.fields['password2'].label = "再次输入密码"
		c["form"] = form
		return render_to_response('index.html', c)

def auth_view(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)
	currentPath = request.POST.get('currentPath', '')
	currentPath = currentPath.replace("invalid/", "").replace("registered/", "")
	if user is not None:
		auth.login(request, user)
		if "log" in currentPath:
			return HttpResponseRedirect(currentPath)
		else:
			return HttpResponseRedirect('/loggedin')
	else:
		if "log" in currentPath:
			return HttpResponseRedirect(currentPath + "invalid")
		else:
			return HttpResponseRedirect('/invalid')

@login_required(login_url="/")
def loggedin(request):
	try: 
		meeting = request.user.meetings_organized.order_by('-pub_date')[0]
		return HttpResponseRedirect('/loggedin/organized/%s/' % meeting.meeting_id)
	except IndexError:
		organized_list = request.user.meetings_organized.all()
		invited_list = request.user.meetings_invited.all()
		return render_to_response('loggedin.html', {'user': request.user, 'list_organized': organized_list, 'list_invited': invited_list,})

def invalid_login(request):
	c = {}
	c.update(csrf(request))
	form = MyRegistrationForm()
	form.fields['password1'].label = "密码"
	form.fields['password2'].label = "再次输入密码"
	c["form"] = form
	c['last_invalid'] = True
	return render_to_response('index.html', c)

def logout(request):
	auth.logout(request)
	c = {}
	c.update(csrf(request))
	form = MyRegistrationForm()
	form.fields['password1'].label = "密码"
	form.fields['password2'].label = "再次输入密码"
	c["form"] = form
	return render_to_response('index.html', c)

def register_user(request):
	currentPath = request.POST.get('currentPath', '')
	currentPath = currentPath.replace("invalid/", "").replace("registered/", "")
	username=request.POST.get('email')
	password=request.POST.get('password1')
	if request.method == 'POST':
		form = MyRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			user = auth.authenticate(username=username, password=password)

			if user is not None:
				auth.login(request, user)
			if "log" in currentPath:
				return HttpResponseRedirect(currentPath)
			else:
				return HttpResponseRedirect('/register_success')
		elif "log" in currentPath:
			return HttpResponseRedirect(currentPath + "registered")
	else:
		form = MyRegistrationForm()
		form.fields['password1'].label = "密码"
		form.fields['password2'].label = "再次输入密码"
	args = {}
	args.update(csrf(request))
	
	args['form'] = form
	
	return render_to_response('register.html', args)


def register_success(request):
	return HttpResponseRedirect('/loggedin')