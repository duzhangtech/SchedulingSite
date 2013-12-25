from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.core.context_processors import csrf
from forms import MyRegistrationForm
from django.contrib.auth.decorators import login_required

def index(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('index.html', c)

def auth_view(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)

	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect('/loggedin')
	else:
		return HttpResponseRedirect('/invalid')

@login_required(login_url="/")
def loggedin(request):
	organized_list = request.user.meetings_organized.all()
	invited_list = request.user.meetings_invited.all()
	return render_to_response('loggedin.html', {'user': request.user, 'list_organized': organized_list, 'list_invited': invited_list,})

def invalid_login(request):
	c = {}
	c.update(csrf(request))
	c['last_invalid'] = True
	return render_to_response('index.html', c)

def logout(request):
	auth.logout(request)
	c = {}
	c.update(csrf(request))
	return render_to_response('index.html', c)

def register_user(request):
	if request.method == 'POST':
		form = MyRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/register_success')
		
	else:
		form = MyRegistrationForm()
	args = {}
	args.update(csrf(request))
	
	args['form'] = form
	
	return render_to_response('register.html', args)



def register_success(request):
	c = {}
	c.update(csrf(request))
	c['last_registered'] = True
	return render_to_response('index.html', c)