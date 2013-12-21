from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from forms import UserProfileForm
from django.contrib.auth.decorators import login_required

@login_required
# what will this do if my login page is not named login???
def user_profile(request):
	if request.method == 'POST':
		form = UserProfileForm(request.POST, instance=request.user.profile)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/loggedin')
	else:
		form = UserProfileForm(instance=request.user.profile)
		
	args = {}
	args.update(csrf(request))
	
	args['form'] = form
	
	return render_to_response('profile.html', args)   


