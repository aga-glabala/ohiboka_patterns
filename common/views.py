from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from common.models import UserProfile
from bracelet.models import Photo, Rate, BraceletCategory, Bracelet
from django.utils.translation import ugettext as _
from common import captcha
from django.conf import settings
from django.contrib.auth.models import User
from common.forms import UserCreationFormExtended, ContactForm
from django.http import HttpResponseRedirect
# from django.core.mail import send_mail
from common.bracelet_tools import get_colors, find_bracelets, get_all_bracelets
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate, login, logout
from pyfb.pyfb import Pyfb
from common.utils import FacebookBackend
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def get_context(request):
    context = {'loginform': AuthenticationForm(), "FACEBOOK_APP_ID": settings.FACEBOOK_APP_ID}
    if request.user.is_authenticated():
        try:
            context['userprofile'] = UserProfile.objects.get(user=request.user)
        except ObjectDoesNotExist:
            pass
    return context


def register(request):
    form = None
    if request.method == 'POST':
        captcha_response = captcha.submit(request.POST['recaptcha_challenge_field'],
                    request.POST['recaptcha_response_field'], settings.RECAPTCHA_PRIVATE_KEY,
                    request.META['REMOTE_ADDR'])
        if captcha_response.is_valid:
            form = UserCreationFormExtended(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, _('Success! You can log in now.'))
                return HttpResponseRedirect('/')
            else:
                messages.error(request, _("An error has occured. Correct entered data."))
        else:
            messages.error(request, _("Wrong captcha, try again."))
    form = UserCreationFormExtended(request.POST)
    context = get_context(request)
    context.update({'form': form, 'captcha': captcha.displayhtml(settings.RECAPTCHA_PUBLIC_KEY)})
    return render_to_response("common/register.html", context,
                              context_instance=RequestContext(request))


@login_required
def userprofile(request):
    if request.user.is_authenticated():
        bracelets = get_all_bracelets(0, request.user, False)
        bracelets_accepted = []
        bracelets_not_accepted = []
        bracelets_private = []
        bracelets_rejected = [] # FIXME
        for br in bracelets:
            if not br.public:
                bracelets_private.append(br)
            if br.accepted:
                bracelets_accepted.append(br)
            else:
                bracelets_not_accepted.append(br)

        photos = request.user.photos
        photos_accepted = []
        photos_not_accepted = []
        for p in photos.all():
            if p.accepted:
                photos_accepted.append(p)
            else:
                photos_not_accepted.append(p)

        context = get_context(request)
#        context['bracelets_accepted'] = Bracelet.objects.accepted(request.user)
#        context['bracelets_not_accepted'] = Bracelet.objects.waiting(request.user)
#        context['bracelets_rejected'] = Bracelet.objects.rejected(request.user)
#        context['bracelets_private'] = Bracelet.objects.private(request.user)
        context['bracelets_accepted'] = bracelets_accepted
        context['bracelets_not_accepted'] = bracelets_not_accepted
        context['bracelets_private'] = bracelets_private
        context['bracelets_rejected'] = bracelets_rejected
        context['photos_accepted'] = photos_accepted
        context['photos_not_accepted'] = photos_not_accepted
        context['rates'] = Rate.objects.filter(user=request.user)
        return render_to_response("common/userprofile.html", context,
                                  RequestContext(request))
    else:
        messages.error(request, _('You need to be logged in.'))
        return HttpResponseRedirect('/')


def user(request, user_name):
    try:
        user = User.objects.get(username=user_name)
    except ObjectDoesNotExist:
        messages.error(request, _('There is no user with login: {0}').format(user_name))
        return HttpResponseRedirect('/')

    context = get_context(request)
    context['user_content'] = user
    context['bracelets'] = get_all_bracelets(0, user)
    context['photos'] = user.photos.filter(accepted=True)
    return render_to_response('common/user.html', context,
                              RequestContext(request))


def about(request, context={}):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        captcha_response = captcha.submit(request.POST['recaptcha_challenge_field'],
                    request.POST['recaptcha_response_field'], settings.RECAPTCHA_PRIVATE_KEY,
                    request.META['REMOTE_ADDR'])
        if captcha_response.is_valid:
            if form.is_valid():
                subject = form.cleaned_data['subject']
                msg_content = form.cleaned_data['message']
                sender = form.cleaned_data['sender']
                receiver = ['aga@ohiboka.com']
                EmailMessage(subject, msg_content, sender, receiver,
                             headers={'Reply-To': sender}).send()
                # send_mail(subject, msg_content, sender, receiver)
                return HttpResponseRedirect('/contact/success/')
            else:
                messages.error(request, _("An error has occured. Correct entered data."))
                # return about(request, {'subject':
                # form.cleaned_data['subject'], 'msg_content':
                # form.cleaned_data['message'], 'sender':
                # form.cleaned_data['sender']})
                context.update(get_context(request))
                context.update({'contactform': form, 'captcha':
                        captcha.displayhtml(settings.RECAPTCHA_PUBLIC_KEY)})
                return render_to_response('common/about.html', context,
                                          RequestContext(request))
        else:
            messages.error(request, _('Wrong captcha.'))
            # return about(request, {'subject': form.cleaned_data['subject'],
            # 'msg_content': form.cleaned_data['message'], 'sender':
            # form.cleaned_data['sender']})
            context.update(get_context(request))
            context.update({'contactform': form, 'captcha':
                        captcha.displayhtml(settings.RECAPTCHA_PUBLIC_KEY)})
            return render_to_response('common/about.html', context,
                                      RequestContext(request))
    else:
        form = ContactForm()
    context.update(get_context(request))
    context.update({'contactform': form, 'captcha': captcha.displayhtml(settings.RECAPTCHA_PUBLIC_KEY)})
    return render_to_response('common/about.html', context,
                              RequestContext(request))


def privacypolicy(request):
    return render_to_response('common/privacypolicy.html',
                              get_context(request), RequestContext(request))


def index(request, context_={}):
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

    return render_to_response('common/index.html', context,
                              RequestContext(request))


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_user(request):
    if 'username' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            messages.success(request, _('You are logged in now'))
            if not request.POST.get('remember_me', None):
                request.session.set_expiry(0)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def facebook_login(request):
    facebook = Pyfb(settings.FACEBOOK_APP_ID)
    facebook.set_permissions("")
    return HttpResponseRedirect(facebook.get_auth_code_url(redirect_uri=settings.FACEBOOK_REDIRECT_URL))


# This view must be refered in your FACEBOOK_REDIRECT_URL. For example:
# http://www.mywebsite.com/facebook_login_success/
def facebook_login_success(request):
    code = request.GET.get('code')
    facebook = Pyfb(settings.FACEBOOK_APP_ID)
    facebook.set_permissions("")
    facebook.get_access_token(settings.FACEBOOK_SECRET_KEY, code,
                              redirect_uri=settings.FACEBOOK_REDIRECT_URL)
    me = facebook.get_myself()
    authenticator = FacebookBackend()
    user = authenticator.authenticate(me)
    login(request, user)
    return HttpResponseRedirect('/')


def setlang(request, lang):
    request.session['django_language'] = lang
    if request.META.get('HTTP_REFERER'):
        r = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        r.set_cookie('django_language', lang)
        return r
    else:
        return HttpResponseRedirect('/')


def search(request):
    # TODO bracelets filter
    url = request.get_full_path()
    if url.find("page") > -1:
            url = url[url.find("&"):]
    else:
        url = "&" + url[url.find("?") + 1:]

    context = get_context(request)
    context.update({'category': request.GET['category'],
                    'difficulty': request.GET['difficulty'],
                    'rate': request.GET['rate'],
                    'color': request.GET['color'],
                    'orderby': request.GET['orderby'],
                    'categories': BraceletCategory.objects.all(),
                    'photo': 'photo' in request.GET,
                    'colors': get_colors(),
                    'search': True,
                    'url': url
                    })

    bracelets = find_bracelets(
        category=request.GET['category'], difficulty=request.GET['difficulty'],
        color=request.GET['color'], orderby=request.GET['orderby'], photo='photo' in request.GET, rate=request.GET['rate'])

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
