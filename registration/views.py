from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from registration.models import UserProfile
from bracelet.views import home, index
from bracelet.bracelet_tools import get_all_bracelets
from bracelet.models import Photo, Rate, Bracelet, BraceletString, BraceletKnot
from django.utils.translation import ugettext as _
from registration import captcha
from settings import RECAPTCHA_PRIVATE_KEY, RECAPTCHA_PUBLIC_KEY
from django.contrib.auth.models import User

def register(request):
	form = None
	error = None
	if request.method == 'POST':
		captcha_response = captcha.submit(request.POST['recaptcha_challenge_field'], request.POST['recaptcha_response_field'],
                                          RECAPTCHA_PRIVATE_KEY, request.META['REMOTE_ADDR'])
		if captcha_response.is_valid:
			form = UserCreationForm(request.POST)
			if form.is_valid():
				form.save()
				return  index(request, {'ok_message': _('Success! You can log in now.')})
			else:
				error = _("An error has occured. Correct entered data.")
		else:
			error = _("Wrong captcha, try again.")
	form = UserCreationForm()
	return render_to_response("registration/register.html", {'form': form, 'loginform': AuthenticationForm(), 'error_message': error,
                               'captcha': captcha.displayhtml(RECAPTCHA_PUBLIC_KEY)}, context_instance = RequestContext(request))

def userprofile(request, error_message = "", ok_message = ""):
	if request.user.is_authenticated():
		bracelets = get_all_bracelets(0, request.user, False)
		accepted = []
		not_accepted = []
		for br in bracelets:
			if br.accepted:
				accepted.append(br)
			else:
				not_accepted.append(br)
		context = {}
		context['loginform'] = AuthenticationForm()
		context['accepted'] = accepted
		context['not_accepted'] = not_accepted
		context['photos'] = Photo.objects.filter(user = request.user)
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
	except Exception, e:
		return index(request, {'error_message': _('There is no user with id: {0}').format(user_id)})

	context = {}
	context['user'] = user
	context['bracelets'] = get_all_bracelets(0, user)
	context['photos'] = Photo.objects.filter(user = user)
	return render_to_response('registration/user.html', context, RequestContext(request))
