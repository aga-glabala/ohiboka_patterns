from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from registration.models import UserProfile
from bracelet.views import index
from bracelet.bracelet_tools import get_all_bracelets
from bracelet.models import Photo, Rate, Bracelet, BraceletString, BraceletKnot
from django.utils.translation import ugettext as _
from registration import captcha
from django.conf import settings
from django.contrib.auth.models import User
from registration.forms import UserCreationFormExtended, ContactForm
from django.http import HttpResponseRedirect
from django.core.mail import send_mail

context = {'loginform' : AuthenticationForm()}
def register(request):
	form = None
	error = None
	if request.method == 'POST':
		captcha_response = captcha.submit(request.POST['recaptcha_challenge_field'], request.POST['recaptcha_response_field'],
                                          settings.RECAPTCHA_PRIVATE_KEY, request.META['REMOTE_ADDR'])
		if captcha_response.is_valid:
			form = UserCreationFormExtended(request.POST)
			if form.is_valid():
				form.save()
				return  index(request, {'ok_message': _('Success! You can log in now.')})
			else:
				error = _("An error has occured. Correct entered data.")
		else:
			error = _("Wrong captcha, try again.")
	form = UserCreationFormExtended()
	context.update({'form': form, 'loginform': AuthenticationForm(), 'error_message': error,
                               'captcha': captcha.displayhtml(settings.RECAPTCHA_PUBLIC_KEY)})
	return render_to_response("registration/register.html", context, context_instance = RequestContext(request))

def userprofile(request, error_message = "", ok_message = ""):
	if request.user.is_authenticated():
		bracelets = get_all_bracelets(0, request.user, False)
		bracelets_accepted = []
		bracelets_not_accepted = []
		for br in bracelets:
			if br.accepted:
				bracelets_accepted.append(br)
			else:
				bracelets_not_accepted.append(br)

		photos = Photo.objects.filter(user = request.user)
		photos_accepted = []
		photos_not_accepted = []
		for p in photos:
			if p.accepted:
				photos_accepted.append(p)
			else:
				photos_not_accepted.append(p)
		context['bracelets_accepted'] = bracelets_accepted
		context['bracelets_not_accepted'] = bracelets_not_accepted
		context['photos_accepted'] = photos_accepted
		context['photos_not_accepted'] = photos_not_accepted
		context['rates'] = Rate.objects.filter(user = request.user)
		if error_message:
			context['error_message'] = error_message
		if ok_message:
			context['ok_message'] = ok_message
		try:
			context['userprofile'] = UserProfile.objects.get(user = request.user)
		except:
			pass
		return render_to_response("registration/userprofile.html", context, RequestContext(request))
	else:
		return index(request, {'error_message': _('You need to be logged in.')})

def delete_bracelet(request, bracelet_id):
	try:
		bracelet = Bracelet.objects.get(id = bracelet_id)
	except:
		return userprofile(request, error_message = _("There is no bracelet with id: {0}").format(bracelet_id))
	if not request.user.is_authenticated():
		return userprofile(request, error_message = _("You need to be logged in to edit bracelets."))
	if bracelet.user != request.user:
		return userprofile(request, error_message = _("You are not owner of this bracelet."))
	strings = BraceletString.objects.filter(bracelet = bracelet)
	for string in strings:
		string.delete()

	knots = BraceletKnot.objects.filter(bracelet = bracelet)
	for knot in knots:
		knot.delete()

	photos = Photo.objects.filter(bracelet = bracelet)
	for photo in photos:
		photo.delete()

	rates = Rate.objects.filter(bracelet = bracelet)
	for rate in rates:
		rate.delete()

	bracelet.delete()
	return userprofile(request, ok_message = _("Bracelet deleted successfully."))

def delete_photo(request, photo_id):
	try:
		photo = Photo.objects.get(id = photo_id)
	except:
		return userprofile(request, error_message = _("There is no photo with id: {0}.").format(photo_id))
	if not request.user.is_authenticated():
		return userprofile(request, error_message = _("You need to be logged in to edit bracelets."))
	if photo.user != request.user:
		return userprofile(request, error_message = _("You are not owner of this photo."))
	photo.delete()
	return userprofile(request, ok_message = _("Photo deleted successfully."))

def delete_rate(request, rate_id):
	try:
		rate = Rate.objects.get(id = rate_id)
	except:
		return userprofile(request, error_message = _("There is no rate with id: {0}.").format(rate_id))
	if not request.user.is_authenticated():
		return userprofile(request, error_message = _("You need to be logged in to edit rates."))
	if rate.user != request.user:
		return userprofile(request, error_message = _("You are not owner of this rate."))
	rate.delete()
	return userprofile(request, ok_message = _("Rate deleted successfully."))

def user(request, user_id):
	try:
		user = User.objects.get(id = user_id)
	except Exception:
		return index(request, {'error_message': _('There is no user with id: {0}').format(user_id)})

	context = {}
	context['user'] = user
	context['bracelets'] = get_all_bracelets(0, user)
	context['photos'] = Photo.objects.filter(user = user, accepted = True)
	return render_to_response('registration/user.html', context, RequestContext(request))

def about(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			send_mail('Subject here', 'Here is the message.', 'from@example.com', fail_silently = DEBUG)
			return HttpResponseRedirect('/thanks/')
	else:
		form = ContactForm()
	context.update({'contactform':form})

	return render_to_response('registration/about.html', context, RequestContext(request))

def privacypolicy(request):
	return render_to_response('registration/privacypolicy.html', context, RequestContext(request))
