# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from bracelet.models import BraceletColor, Bracelet, BraceletCategory, \
	BraceletString, BraceletKnot, BraceletKnotType, Photo, Rate
import datetime
from bracelet.pattern_tools import BraceletPattern
from common.bracelet_tools import get_colors
from bracelet.forms import UploadFileForm
from bracelet.helper import handle_uploaded_file, scale
from django.utils.translation import ugettext as _
from django.utils.translation import gettext
import gettext as gt
from django.conf import settings
import time
from django.core.exceptions import ObjectDoesNotExist
from common.views import userprofile, index, get_context
import unicodedata
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage


def add(request, context_ = {}):
	context = {'colors': get_colors(),
			'categories': BraceletCategory.objects.all(),
			}
	context.update(context_)
	context.update(get_context(request))
	return render_to_response('bracelet/add.html', context, RequestContext(request))

def bracelet(request, bracelet_url, context = {}):
	try:
		bracelet = Bracelet.objects.get(url = bracelet_url)
	except ObjectDoesNotExist:
		return index(request, {'error_message':_('There is no bracelet with this id.')})
	bp = BraceletPattern(bracelet)
	bp.generate_pattern()
	context.update(get_context(request))

	texts = [gettext(s.text) for s in BraceletKnotType.objects.all().order_by('id')]
	context.update({'bracelet': bracelet,
			'style':bp.get_style(),
			'nofstr':bp.get_n_of_strings(),
			'knotsType':bp.get_knots_types(),
			'knotsColor':bp.get_knots_colors(),
			'strings':bp.get_strings(),
			'nofrows':bp.nofrows,
			'texts':texts,
			'ifwhite':bp.get_ifwhite(),
			'nofphotos': len(Photo.objects.filter(bracelet = bracelet, accepted = True)),
			'request': request,
			})
	if 'message' in context:
		del context['message']
	if not bracelet.public:
		context['message'] = _("""This bracelet is private. It means you can see it only if you have link to this page.""")
	elif bracelet.accepted == 0:
		context['message'] = _("""This bracelet is not accepted yet. It means you can see it only if you have link to this page.""")
	elif bracelet.accepted == -1:
		context['message'] = _("""This bracelet has been rejected. It means you can see it only if you have link to this page.""")
	rates = []
	if request.user.is_authenticated():
		rates = Rate.objects.filter(user = request.user, bracelet = bracelet)
	if len(rates) > 0:
		context['rate'] = rates[0].rate
	elif 'rate' in context:
		del context['rate']

	if 'change_status' in request.GET:
		context['ok_message'] = _('Bracelet\'s status was successfully changed') + '.'
	elif 'ok_message' in context and context['ok_message'] == _('Bracelet\'s status was successfully changed') + '.':
		del context['ok_message']

	return render_to_response('bracelet/bracelet.html', context, RequestContext(request))

@login_required
def addpattern(request):
	if not request.POST['name']:
		return add(request, {'error_message':_('You need to set name to bracelet')})
	colors_tmp = request.POST['colors'][:-1].split(' ')
	colors = []
	for c in colors_tmp:
		colors.append((int('0x' + c[1:], 16)))
	knots = request.POST['pattern'].split()
	url = unicodedata.normalize('NFKD', request.POST['name'].lower().replace(' ', '_')).encode('ascii', 'ignore')

	brs = Bracelet.objects.filter(url__contains = url)
	if brs:
		url += '-' + str(len(brs))

	if request.POST['public'] == '1':
		public = True
	else:
		public = False
	b = Bracelet(user = request.user, date = datetime.datetime.today(), url = url, public = public, name = request.POST['name'], accepted = False, difficulty = request.POST['difficulty'], category = BraceletCategory.objects.filter(name = request.POST['category'])[0], rate = 0)

	b.save()
	index = 0
	for color in colors:
		bs = BraceletString(index = index, color = BraceletColor.objects.filter(hexcolor = color)[0], bracelet = b)
		index += 1
		bs.save()
	for i in range(len(knots)):
		bk = BraceletKnot(bracelet = b, knottype = BraceletKnotType.objects.filter(id = knots[i])[0], index = i)
		bk.save()

	photo_name = str(int(time.time() * 1000)) + "-" + str(b.id) + '.png'
	bp = BraceletPattern(b.id)
	bp.generate_pattern()
	bp.generate_photo(settings.MEDIA_ROOT + 'images/' + photo_name)
	scale(photo_name, settings.MEDIA_ROOT + 'images/', settings.MEDIA_ROOT + 'bracelet_thumbs/')
	photo = Photo(user = request.user, name = photo_name, accepted = True, bracelet = b)
	photo.save()

	b.photo_id = photo.id
	b.save()
	return bracelet(request, b.url, {'ok_message':_('Bracelet was successfully saved.')})

def photos(request, bracelet_id):
	photos = Photo.objects.filter(bracelet = Bracelet.objects.get(id = bracelet_id), accepted = True)
	form = UploadFileForm()
	return render_to_response('bracelet/tabs/photos.html', {'form': form, 'bracelet_id':bracelet_id, 'photos':photos, 'selectTab':3}, RequestContext(request))

@login_required
def photo_upload(request, bracelet_id):
	try:
		bracelet_obj = Bracelet.objects.get(id = bracelet_id)
	except ObjectDoesNotExist:
		return index(request, {'error_message':_('There is no bracelet with this id {0}').format(bracelet_id)})

	photos = Photo.objects.filter(bracelet = bracelet_obj, accepted = True)
	form = UploadFileForm(request.POST, request.FILES)
	if form.is_valid():
		handle_uploaded_file(request.FILES['file'], request.POST['bracelet_id'], request.user)
		return bracelet(request, bracelet_obj.url, {'form': form, 'bracelet_id':bracelet_id, 'photos':photos, 'selectTab':3, 'ok_message':_('Photo was uploaded successfully. It will show up here after admin acceptance.')})
	return bracelet(request, bracelet_obj.url, {'form': form, 'bracelet_id':bracelet_id, 'photos':photos, 'selectTab':3, 'error_message':_('Error has occured when uploading photo, choose photo and try again.')})

@login_required
def rate(request, bracelet_id, bracelet_rate):
	try:
		rate = int(bracelet_rate)
	except ValueError:
		return HttpResponse(_("Rate is not a number"))
	if rate < 1 or rate > 5:
		return HttpResponse(_("Rate must be between 1 and 5"))
	if request.user.is_authenticated():
		bracelet = Bracelet.objects.get(id = bracelet_id)
		if bracelet != None:
			rates = Rate.objects.filter(user = request.user, bracelet = bracelet)
			if len(rates) == 0:
				r = Rate(user = request.user, bracelet = bracelet, rate = rate)
				r.save()
			else:
				rates[0].rate = rate
				rates[0].save()
			rates = Rate.objects.filter(bracelet = bracelet)
			sum_rates = 0
			for rate in rates:
				sum_rates += rate.rate
			bracelet.rate = float(sum_rates) / len(rates)
			bracelet.save()
			return HttpResponse("OK")
		else:
			return HttpResponse(_("Pattern do not exist"))
	return HttpResponse(_("You need to be logged in to rate patterns"))


@login_required
def delete_bracelet(request, bracelet_id):
	try:
		b = Bracelet.objects.get(id = bracelet_id)
	except ObjectDoesNotExist:
		return index(request, {'error_message': _('Bracelet do not exists') + '!'})
	if b.user != request.user:
		return index(request, {'error_message': _('This bracelet is not yours') + '!'})
	b.deleted = True
	b.save()
	return index(request, {'ok_message': _('Bracelet was successfully deleted') + '.'})

@login_required
def change_status(request, bracelet_id):
	try:
		b = Bracelet.objects.get(id = bracelet_id)
	except ObjectDoesNotExist:
		return index(request, {'error_message': _('Bracelet do not exists') + '!'})
	if b.user != request.user:
		return index(request, {'error_message': _('This bracelet is not yours') + '!'})
	b.public = not b.public
	b.save()
	return HttpResponseRedirect('/bracelet/{0}?change_status=ok'.format(b.url))

@login_required
def accept(request, bracelet_id, bracelet_status):
	try:
		b = Bracelet.objects.get(id = bracelet_id)
	except ObjectDoesNotExist:
		return index(request, {'error_message': _('Bracelet do not exists') + '!'})
	if not request.user.is_staff:
		return index(request, {'error_message': _('This bracelet is not yours') + '!'})
	try:
		status = int(bracelet_status)
	except ValueError:
		return index(request, {'error_message': _('Wrong value for bracelet status') + '!'})
	if not status in [-1, 0, 1]:
		return index(request, {'error_message': _('Wrong value for bracelet status') + '!'})
	b.accepted = status
	b.save()
	msg_content = ''
	if status == -1:
		subject = 'Your bracelet was rejected | Twoja bransoletka została odrzucona'
		msg_content = 'Hey! I\'m sorry, but your bracelet was rejected. It was probably to easy or same pattern was already submitted. You can still see this bracelet from your profile'+\
						' (http://patterns.ohiboka.com/profile). Thanks for using my site and hope to see you again.'+\
						'\r\nGo to pattern: http://patterns.ohiboka.com/bracelet/{0}'+\
						'\r\nAdd new bracelet: http://patterns.ohiboka.com/add'+\
						'\r\nRegards,'+\
						'\r\nAga'+\
						'\r\nhttp://ohiboka.com'+\
						'\r\n\r\n----\r\n\r\n'+\
						'Cześć, przykro mi, ale Twoja bransoletka została odrzucona. Prawdopodobnie była zbyt prosta lub jest już taka na stronie. Ciągle możesz ją zobaczyć na swoim profilu'+\
						' (http://patterns.ohiboka.com/profile). Dziekuję za skorzystanie z mojej strony i mam nadzieję że jeszcze kiedyś tu zajrzysz.'+\
						'\r\nZobacz wzór: http://patterns.ohiboka.com/bracelet/{0}'+\
						'\r\nDodaj nowy wzór: http://patterns.ohiboka.com/add'+\
						'\r\nPozdrowienia,'+\
						'\r\nAga'+\
						'\r\nhttp://ohiboka.com'+\
		EmailMessage(subject, msg_content, ['aga@ohiboka.com'], b.user.email, headers = {'Reply-To': 'aga@ohiboka.com'}).send()
	elif status == 1:
		subject = 'Your bracelet was accepted | Twoja bransoletka została zaakceptowana'
		msg_content = 'Hey! Congratulations, your bracelet was accepted. Thanks for great pattern. You can see this bracelet from your profile and on main page'+\
						' (http://patterns.ohiboka.com/profile and http://patterns.ohiboka.com). Thanks for using my site and hope to see you again.'+\
						'\r\nGo to pattern: http://patterns.ohiboka.com/bracelet/{0}'+\
						'\r\nAdd new bracelet: http://patterns.ohiboka.com/add'+\
						'\r\nRegards,'+\
						'\r\nAga'+\
						'\r\nhttp://ohiboka.com'+\
						'\r\n\r\n----\r\n\r\n'+\
						'Cześć! Gratulacje, Twoja bransoletka została zaakceptowana. Dzięki za świetny wzór. Możesz zobaczyć wzór na swoim profilu i na stronie głównej'+\
						' (http://patterns.ohiboka.com/profile and http://patterns.ohiboka.com). Dzięki za korzystanie ze strony i do zobaczenia ponownie.'+\
						'\r\nZobacz wzór: http://patterns.ohiboka.com/bracelet/{0}'+\
						'\r\nDodaj nowy wzór: http://patterns.ohiboka.com/add'+\
						'\r\nPozdrowienia,'+\
						'\r\nAga'+\
						'\r\nhttp://ohiboka.com'
	EmailMessage(subject, msg_content, 'ohiboka@ohiboka.com', [b.user.email], headers = {'Reply-To': ['aga@ohiboka.com']}).send()
	return bracelet(request, b.url, {'ok_message': _('Bracelet\'s status was successfully changed') + '.'})

@login_required
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

@login_required
def delete_rate(request, rate_id):
	try:
		rate = Rate.objects.get(id = rate_id)
	except:
		return userprofile(request, error_message = _("There is no rate with id: {0}.").format(rate_id))
	if not request.user.is_authenticated():
		return userprofile(request, error_message = _("You need to be logged in to edit rates."))
	if rate.user != request.user:
		return userprofile(request, error_message = _("You are not owner of this rate."))

	bracelet = Bracelet.objects.get(id = rate.bracelet.id)
	rate.delete()
	bracelet.rate = bracelet.get_average_rate()
	bracelet.save()

	return userprofile(request, ok_message = _("Rate deleted successfully."))

def _fake_for_translate():
	_("Make one knot {0} in forward on {1}")
	_("Make one knot {0} in backward on {1}")
	_("Make one knot {0} in forward-backward on {1}")
	_("Make one knot {0} in backward-forward on {1}")