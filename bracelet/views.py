# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from bracelet.models import BraceletColor, Bracelet, BraceletCategory, \
    BraceletString, BraceletKnot, BraceletKnotType, Photo, Rate
import datetime
from bracelet.pattern_tools import BraceletPattern, get_custom_characters
from common.bracelet_tools import get_colors
from bracelet.forms import UploadFileForm
from bracelet.helper import handle_uploaded_file, scale, delete_image_file
from django.utils.translation import ugettext as _
from django.utils.translation import gettext
from django.utils import simplejson
from django.conf import settings
import time
from django.core.exceptions import ObjectDoesNotExist
from common.views import get_context
import unicodedata
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.contrib import messages
import re

def add(request, bracelet_type, context_ = {}):
    context = {
            'colors': get_colors(),
            'characters': get_custom_characters(),
            'categories': BraceletCategory.objects.all(),
            'bracelet': None,
            'nofrows': 10,
            'nofstr': 5,
            'braceletType': 2 if bracelet_type == 'straight'  else 1,
            'knotsType': [],
            'stringColors': [],
            'ifwhite': []
            }
    context.update(context_)
    context.update(get_context(request))
    return render_to_response('bracelet/add.html', context, RequestContext(request))

def bracelet(request, bracelet_url, context = {}):
    try:
        bracelet = Bracelet.objects.get(url = bracelet_url)
    except ObjectDoesNotExist:
        messages.error(request, _('There is no bracelet with this id.'))
        return HttpResponseRedirect('/')
    bp = BraceletPattern(bracelet)
    bp.generate_pattern()
    context.update(get_context(request))

    texts = [gettext(s.text) for s in BraceletKnotType.objects.all().order_by('id')]
    context.update({'bracelet': bracelet,
            'style':bp.get_style(),
            'braceletType':bp.bracelet.type,
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
        messages.info(request, _("""This bracelet is private. It means you can see it only if you have link to this page."""))
    elif bracelet.accepted == 0:
        messages.info(request, _("""This bracelet is not accepted yet. It means you can see it only if you have link to this page."""))
    elif bracelet.accepted == -1:
        messages.info(request, _("""This bracelet has been rejected. It means you can see it only if you have link to this page."""))
    rates = []
    if request.user.is_authenticated():
        rates = Rate.objects.filter(user = request.user, bracelet = bracelet)
    if len(rates) > 0:
        context['rate'] = rates[0].rate
    elif 'rate' in context:
        del context['rate']

    if 'change_status' in request.GET:
        messages.success(request, _('Bracelet\'s status was successfully changed'))

    return render_to_response('bracelet/bracelet.html', context, RequestContext(request))

@login_required
def addpattern(request):
    if not request.POST['name']:
        messages.error(request, _('You need to set name to bracelet'))
        return add(request)
    colors_tmp = request.POST['colors'][:-1].split(' ')
    colors = []
    for c in colors_tmp:
        colors.append((int('0x' + c[1:], 16)))
    knots = request.POST['pattern'].split()

    if request.POST['public'] == '1':
        public = True
    else:
        public = False
    if request.POST['bracelet_id']:
        b = Bracelet.objects.filter(id = request.POST['bracelet_id'])[0]
        b.public = public
        b.difficulty = request.POST['difficulty']
        b.category = BraceletCategory.objects.filter(name = request.POST['category'])[0]
        b.accepted = 0
    else:
        url = unicodedata.normalize('NFKD', request.POST['name'].lower()).encode('ascii', 'ignore')
        url = re.sub(r'[^a-zA-Z0-9]', r'_', url)
        url = re.sub(r'_+', '_', url)
        brs = Bracelet.objects.filter(url__startswith = url + '-').order_by('id').reverse()
        if not brs:
            brs = Bracelet.objects.filter(url = url).order_by('id').reverse()
            if brs:
                url += '-1'
        else:
            brs = brs[0]
            url += '-' + str(int(brs.url.split('-')[1]) + 1)
        b = Bracelet(user = request.user, date = datetime.datetime.today(), url = url, public = public, name = request.POST['name'], accepted = False, difficulty = request.POST['difficulty'], category = BraceletCategory.objects.filter(name = request.POST['category'])[0], rate = 0, type = request.POST['type'])
    b.save()
    index = 0
    BraceletString.objects.filter(bracelet = b).delete()
    for color in colors:
        bs = BraceletString(index = index, color = BraceletColor.objects.filter(hexcolor = color)[0], bracelet = b)
        index += 1
        bs.save()
    BraceletKnot.objects.filter(bracelet = b).delete()
    for i in range(len(knots)):
        bk = BraceletKnot(bracelet = b, knottype = BraceletKnotType.objects.filter(id = knots[i])[0], index = i)
        bk.save()

    photo_name = str(int(time.time() * 1000)) + "-" + str(b.id) + '.png'
    bp = BraceletPattern(b)
    bp.generate_pattern()
    bp.generate_photo(settings.MEDIA_ROOT + 'images/' + photo_name)
    scale(photo_name, settings.MEDIA_ROOT + 'images/', settings.MEDIA_ROOT + 'bracelet_thumbs/')
    if b.photo_id:
        photo = Photo.objects.filter(id = b.photo_id)[0]
        delete_image_file(photo.name)
        photo.name = photo_name
        photo.save()
    else:
        photo = Photo(user = request.user, name = photo_name, accepted = True, bracelet = b)
        photo.save()
        b.photo_id = photo.id
        b.save()
    messages.success(request, _('Bracelet was successfully saved.'))
    return bracelet(request, b.url)

def photos(request, bracelet_id):
    photos = Photo.objects.filter(bracelet = Bracelet.objects.get(id = bracelet_id), accepted = True)
    form = UploadFileForm()
    return render_to_response('bracelet/tabs/photos.html', {'form': form, 'bracelet_id':bracelet_id, 'photos':photos, 'selectTab':3}, RequestContext(request))

@login_required
def photo_upload(request, bracelet_id):
    try:
        bracelet_obj = Bracelet.objects.get(id = bracelet_id)
    except ObjectDoesNotExist:
        messages.error(request, _('There is no bracelet with this id {0}').format(bracelet_id))
        return HttpResponseRedirect('/')

    photos = Photo.objects.filter(bracelet = bracelet_obj, accepted = True)
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        handle_uploaded_file(request.FILES['file'], request.POST['bracelet_id'], request.user)
        messages.success(request, _('Photo was uploaded successfully. It will show up here after admin acceptance.'))
        return HttpResponseRedirect('/bracelet/' + bracelet_obj.url + '#ui-tabs-2')
    messages.error(request, _('Error has occured when uploading photo, choose photo and try again.'))
    return HttpResponseRedirect('/bracelet/' + bracelet_obj.url + '#ui-tabs-2')

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
def edit_bracelet(request, bracelet_id, context = {}):
    try:
        bracelet = Bracelet.objects.get(id = bracelet_id)
    except ObjectDoesNotExist:
        messages.error(request, _('There is no bracelet with this id.'))
        return HttpResponseRedirect('/')
    bp = BraceletPattern(bracelet)
    bp.generate_pattern()
    context.update(get_context(request))
    context.update({'bracelet': bracelet,
            'stringColors':bp.get_colors(),
            'braceletType':bp.bracelet.type,
            'nofstr':bp.get_n_of_strings(),
            'knotsType':bp.get_knots_types(),
            'nofrows':bp.nofrows,
            'ifwhite':bp.get_ifwhite(),
            'nofphotos': len(Photo.objects.filter(bracelet = bracelet, accepted = True)),
            'request': request,
            'colors': get_colors(),
            'categories': BraceletCategory.objects.all(),
    })
    return render_to_response('bracelet/add.html', context, RequestContext(request))

@login_required
def delete_bracelet(request, bracelet_id):
    try:
        b = Bracelet.objects.get(id = bracelet_id)
    except ObjectDoesNotExist:
        messages.error(request, _('Bracelet do not exists'))
        return HttpResponseRedirect('/')
    if b.user != request.user:
        messages.error(request, _('This bracelet is not yours'))
        return HttpResponseRedirect('/')
    b.deleted = True
    b.save()
    messages.error(request, _('Bracelet was successfully deleted'))
    return HttpResponseRedirect('/')

@login_required
def change_status(request, bracelet_id):
    try:
        b = Bracelet.objects.get(id = bracelet_id)
    except ObjectDoesNotExist:
        messages.error(request, _('Bracelet do not exists'))
        return HttpResponseRedirect('/')
    if b.user != request.user or request.user.is_staff:
        messages.error(request, _('This bracelet is not yours'))
        return HttpResponseRedirect('/')
    b.public = not b.public
    b.save()
    return HttpResponseRedirect('/bracelet/{0}?change_status=ok'.format(b.url))

@login_required
def accept(request, bracelet_id, bracelet_status):
    try:
        b = Bracelet.objects.get(id = bracelet_id)
    except ObjectDoesNotExist:
        messages.error(request, _('This bracelet is not yours'))
        return HttpResponseRedirect('/')
    if not request.user.is_staff:
        messages.error(request, _('You have no permission to accept bracelets'))
        return HttpResponseRedirect('/')
    try:
        status = int(bracelet_status)
    except ValueError:
        messages.error(request, _('Wrong value for bracelet status'))
        return HttpResponseRedirect('/')
    if not status in [-1, 0, 1]:
        messages.error(request, _('Wrong value for bracelet status'))
        return HttpResponseRedirect('/')
    b.accepted = status
    b.save()
    if b.user.email:
        msg_content = ''
        if status == -1:
            subject = 'Your bracelet was rejected | Twoja bransoletka została odrzucona'
            msg_content = u'Hey! I\'m sorry, but your bracelet was rejected. It was probably to easy or same pattern was already submitted. You can still see this bracelet from your profile' + \
                            u' (http://patterns.ohiboka.com/profile). Thanks for using my site and hope to see you again.' + \
                            u'\r\nGo to pattern: http://patterns.ohiboka.com/bracelet/' + b.url + \
                            u'\r\nAdd new bracelet: http://patterns.ohiboka.com/add' + \
                            u'\r\nRegards,' + \
                            u'\r\nAga' + \
                            u'\r\nhttp://ohiboka.com' + \
                            u'\r\n\r\n----\r\n\r\n' + \
                            u'Cześć, przykro mi, ale Twoja bransoletka została odrzucona. Prawdopodobnie była zbyt prosta lub jest już taka na stronie. Ciągle możesz ją zobaczyć na swoim profilu' + \
                            u' (http://patterns.ohiboka.com/profile). Dziekuję za skorzystanie z mojej strony i mam nadzieję że jeszcze kiedyś tu zajrzysz.' + \
                            u'\r\nZobacz wzór: http://patterns.ohiboka.com/bracelet/' + b.url + \
                            u'\r\nDodaj nowy wzór: http://patterns.ohiboka.com/add' + \
                            u'\r\nPozdrowienia,' + \
                            u'\r\nAga' + \
                            u'\r\nhttp://ohiboka.com'
            EmailMessage(subject, msg_content, 'aga@ohiboka.com', [b.user.email], headers = {'Reply-To': ['aga@ohiboka.com']}).send()
        elif status == 1:
            subject = 'Your bracelet was accepted | Twoja bransoletka została zaakceptowana'
            msg_content = u'Hey! Congratulations, your bracelet was accepted. Thanks for great pattern. You can see this bracelet from your profile and on main page' + \
                            u' (http://patterns.ohiboka.com/profile and http://patterns.ohiboka.com). Thanks for using my site and hope to see you again.' + \
                            u'\r\nGo to pattern: http://patterns.ohiboka.com/bracelet/' + b.url + \
                            u'\r\nAdd new bracelet: http://patterns.ohiboka.com/add' + \
                            u'\r\nRegards,' + \
                            u'\r\nAga' + \
                            u'\r\nhttp://ohiboka.com' + \
                            u'\r\n\r\n----\r\n\r\n' + \
                            u'Cześć! Gratulacje, Twoja bransoletka została zaakceptowana. Dzięki za świetny wzór. Możesz zobaczyć wzór na swoim profilu i na stronie głównej' + \
                            u' (http://patterns.ohiboka.com/profile and http://patterns.ohiboka.com). Dzięki za korzystanie ze strony i do zobaczenia ponownie.' + \
                            u'\r\nZobacz wzór: http://patterns.ohiboka.com/bracelet/' + b.url + \
                            u'\r\nDodaj nowy wzór: http://patterns.ohiboka.com/add' + \
                            u'\r\nPozdrowienia,' + \
                            u'\r\nAga' + \
                            u'\r\nhttp://ohiboka.com'
        EmailMessage(subject, msg_content, 'aga@ohiboka.com', [b.user.email], headers = {'Reply-To': ['aga@ohiboka.com']}).send()
    messages.success(request, _('Bracelet\'s status was successfully changed'))
    return bracelet(request, b.url)

@login_required
def delete_photo(request, photo_id):
    try:
        photo = Photo.objects.get(id = photo_id)
    except:
        messages.error(request, _("There is no photo with id: {0}.").format(photo_id))
        return HttpResponseRedirect('/profile')
    if not request.user.is_authenticated():
        messages.error(request, _("You need to be logged in to edit bracelets."))
        return HttpResponseRedirect('/profile')
    if photo.user != request.user:
        messages.error(request, _("You are not owner of this photo."))
        return HttpResponseRedirect('/profile')
    photo.delete()
    delete_image_file(photo.name)
    messages.success(request, _("Photo deleted successfully."))
    return HttpResponseRedirect('/profile')

@login_required
def delete_rate(request, rate_id):
    try:
        rate = Rate.objects.get(id = rate_id)
    except:
        messages.error(request, _("There is no rate with id: {0}.").format(rate_id))
        return HttpResponseRedirect('/profile')
    if not request.user.is_authenticated():
        messages.error(request, _("You need to be logged in to edit rates."))
        return HttpResponseRedirect('/profile')
    if rate.user != request.user:
        messages.error(request, _("You are not owner of this rate."))
        return HttpResponseRedirect('/profile')

    bracelet = Bracelet.objects.get(id = rate.bracelet.id)
    rate.delete()
    bracelet.rate = bracelet.get_average_rate()
    bracelet.save()
    messages.success(request, _("Rate deleted successfully."))
    return HttpResponseRedirect('/profile')

def generate_text_pattern(request, pattern_text, text_height):
    if text_height != "7" and text_height != "10":
        return HttpResponse("Bad text_height parameter value (7 or 10 allowed)", status = 400, mimetype = 'application/json')
    empty = [[5, 5, 5, 5, 5, 5, 5]] if text_height == "7" else [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]
    to_json = []
    to_json += empty
    notfound = []
    characters = simplejson.load(open(settings.PROJECT_ROOT + "/bracelet/" + text_height + ".json"))

    pattern_text = pattern_text.split('\f')
    for char in pattern_text:
        if char not in characters:
            notfound += char
        else:
            to_json += characters[char]
            to_json += empty
    error = None
    if len(notfound) > 0:
        error = _("Not found: ") + " ".join(notfound)
    result = {"pattern": to_json, "error": error}
    return HttpResponse(simplejson.dumps(result), mimetype = 'application/json')

def _fake_for_translate():
    _("Make one knot {0} in forward on {1}")
    _("Make one knot {0} in backward on {1}")
    _("Make one knot {0} in forward-backward on {1}")
    _("Make one knot {0} in backward-forward on {1}")
