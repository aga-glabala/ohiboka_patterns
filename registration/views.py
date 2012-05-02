from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
def register(request):
	form = None
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/")
	else:
		form = UserCreationForm()
	return render_to_response("registration/register.html", {'form': form,'loginform': AuthenticationForm(),},
                          context_instance=RequestContext(request))