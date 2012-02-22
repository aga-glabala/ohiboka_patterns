from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.template.context import RequestContext
from settings import STATIC_URL, STATICFILES_DIRS
def home(request):
	form = AuthenticationForm()
	context = {
		'lista': ("Q", "W", "e"),
		'lista2': ("R", "T", "Y"), 
		'form':form,
	}
	return render_to_response('bracelet/index.html', context, RequestContext(request))

def add(request):
	return HttpResponse("Hello, world. You're at the add page.")

def bracelet(request, bracelet_id):
	return HttpResponse("You're looking at bracelet %s." % bracelet_id)

def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/')

def login_user(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
			# Redirect to a success page.
			print "1"
		else:
			# Return a 'disabled account' error message
			print "2"
	else:
		# Return an 'invalid login' error message.
		print "3"
	return HttpResponseRedirect('/')