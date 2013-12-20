from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.core.context_processors import csrf
from forms import MyRegistrationForm

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

def loggedin(request):
	return render_to_response('loggedin.html', {'full_name': request.user.username})

def invalid_login(request):
	return render_to_response('invalid_login.html')

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
	return render_to_response('register_success.html')