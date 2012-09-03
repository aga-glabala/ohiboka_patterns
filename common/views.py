from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from common.models import UserProfile
from bracelet.models import Photo, Rate, BraceletCategory
from django.utils.translation import ugettext as _
from common import captcha
from django.conf import settings
from django.contrib.auth.models import User
from common.forms import UserCreationFormExtended, ContactForm
from django.http import HttpResponseRedirect
#from django.core.mail import send_mail
from common.bracelet_tools import get_colors, find_bracelets, get_all_bracelets
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate, login, logout
from pyfb.pyfb import Pyfb
from common.utils import FacebookBackend
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required

def get_context(request):
	context = {'loginform': AuthenticationForm(), "FACEBOOK_APP_ID": settings.FACEBOOK_APP_ID}
	if request.user.is_authenticated():
		try:
			context['userprofile'] = UserProfile.objects.get(user = request.user)
		except ObjectDoesNotExist:
			pass
	return context

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
	context = get_context(request)
	context.update({'form': form, 'error_message': error,
                               'captcha': captcha.displayhtml(settings.RECAPTCHA_PUBLIC_KEY)})
	return render_to_response("common/register.html", context, context_instance = RequestContext(request))

@login_required
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

		context = get_context(request)
		context['bracelets_accepted'] = bracelets_accepted
		context['bracelets_not_accepted'] = bracelets_not_accepted
		context['photos_accepted'] = photos_accepted
		context['photos_not_accepted'] = photos_not_accepted
		context['rates'] = Rate.objects.filter(user = request.user)
		if error_message:
			context['error_message'] = error_message
		if ok_message:
			context['ok_message'] = ok_message
		return render_to_response("common/userprofile.html", context, RequestContext(request))
	else:
		return index(request, {'error_message': _('You need to be logged in.')})

'''
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
'''

def user(request, user_name):
	try:
		user = User.objects.get(username = user_name)
	except ObjectDoesNotExist:
		return index(request, {'error_message': _('There is no user with login: {0}').format(user_name)})

	context = get_context(request)
	context['user_content'] = user
	context['bracelets'] = get_all_bracelets(0, user)
	context['photos'] = Photo.objects.filter(user = user, accepted = True)
	return render_to_response('common/user.html', context, RequestContext(request))

def about(request, context = {}, errors = 0):
	if request.method == 'POST' and not errors:
		form = ContactForm(request.POST)
		captcha_response = captcha.submit(request.POST['recaptcha_challenge_field'], request.POST['recaptcha_response_field'],
                                          settings.RECAPTCHA_PRIVATE_KEY, request.META['REMOTE_ADDR'])
		if captcha_response.is_valid:
			if form.is_valid():
				subject = form.cleaned_data['subject']
				msg_content = form.cleaned_data['message']
				sender = form.cleaned_data['sender']
				print 'aaaaaaaa', sender
				receiver = ['aga@ohiboka.com']
				EmailMessage(subject, msg_content, sender, receiver, headers = {'Reply-To': sender}).send()
				#send_mail(subject, msg_content, sender, receiver)
				return HttpResponseRedirect('/contact/success/')
			else:
				return about(request, {'error_message': _("An error has occured. Correct entered data.")}, errors = 1)
		else:
			return about(request, {'error_message': _('Wrong captcha.')}, errors = 1)
	else:
		form = ContactForm()
	context.update(get_context(request))
	context.update({'contactform':form, 'captcha': captcha.displayhtml(settings.RECAPTCHA_PUBLIC_KEY)})
	return render_to_response('common/about.html', context, RequestContext(request))

def privacypolicy(request):
	return render_to_response('common/privacypolicy.html', get_context(request), RequestContext(request))

def index(request, context_ = {}):
	bracelets = get_all_bracelets(0)
	paginator = Paginator(bracelets, 9)
	page = request.GET.get('page')
	if not page:
		page = 1
	try:
		bracelets = paginator.page(page)
	except PageNotAnInteger:
		bracelets = paginator.page(1)
	except EmptyPage:
		bracelets = paginator.page(paginator.num_pages)

	context = get_context(request)
	context.update(context_)
	context.update({
		'patterns': bracelets,
		'colors': get_colors(),
		'categories': BraceletCategory.objects.all(),
	})

	return render_to_response('common/index.html', context, RequestContext(request))

def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/')

def login_user(request):
	if 'username' in request.POST:
		username = request.POST['username']
		password = request.POST['password']
		form = AuthenticationForm(data = request.POST)
		user = authenticate(username = username, password = password)
		if user is not None and user.is_active:
			login(request, user)
		context = {'loginform':form, }
		return index(request, context)
	else:
		index(request)

def facebook_login(request):
	facebook = Pyfb(settings.FACEBOOK_APP_ID)
	return HttpResponseRedirect(facebook.get_auth_code_url(redirect_uri = settings.FACEBOOK_REDIRECT_URL))


#This view must be refered in your FACEBOOK_REDIRECT_URL. For example: http://www.mywebsite.com/facebook_login_success/
def facebook_login_success(request):
	code = request.GET.get('code')
	facebook = Pyfb(settings.FACEBOOK_APP_ID)
	facebook.get_access_token(settings.FACEBOOK_SECRET_KEY, code, redirect_uri = settings.FACEBOOK_REDIRECT_URL)
	me = facebook.get_myself()
	authenticator = FacebookBackend()
	user = authenticator.authenticate(me)
	login(request, user)
	return index(request, {})

def setlang(request, lang):
	request.session['django_language'] = lang
	r = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	r.set_cookie('django_language', lang)
	return r

def search(request):
	# TODO bracelets filter
	url = request.get_full_path()
	if url.find("page") > -1:
			url = url[url.find("&") :]
	else:
		url = "&" + url[url.find("?") + 1:]

	context = get_context(request)
	context.update({'category' : request.GET['category'],
		'difficulty': request.GET['difficulty'],
		'rate': request.GET['rate'],
		'color': request.GET['color'],
		'orderby': request.GET['orderby'],
		'categories': BraceletCategory.objects.all(),
		'photo': 'photo' in request.GET,
		'colors': get_colors(),
		'search': True,
		'url':url
	})

	bracelets = find_bracelets(category = request.GET['category'], difficulty = request.GET['difficulty'],
										color = request.GET['color'], orderby = request.GET['orderby'], photo = 'photo' in request.GET, rate = request.GET['rate'])

	paginator = Paginator(bracelets, 9)
	page = request.GET.get('page')
	if page == None:
		page = 1
	try:
		bracelets = paginator.page(page)
	except PageNotAnInteger:
		bracelets = paginator.page(1)
	except EmptyPage:
		bracelets = paginator.page(paginator.num_pages)
	context['patterns'] = bracelets
	return render_to_response('common/index.html', context, RequestContext(request))

def contact_success(request):
	return render_to_response('contact_ok.html', get_context(request), RequestContext(request))

