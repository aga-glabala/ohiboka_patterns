from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.template.context import RequestContext
from bracelet.models import BraceletColor, Bracelet, BraceletCategory,\
	BraceletString, BraceletKnot, BraceletKnotType, Photo
import datetime
from bracelet.pattern_tools import BraceletPattern
from bracelet.bracelet_tools import get_all_bracelets, find_bracelets,\
	get_colors
from bracelet.forms import UploadFileForm
from bracelet.helper import handle_uploaded_file

def setlang(request, lang):
	request.session['django_language'] = lang
	r = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	r.set_cookie('django_language', lang)
	return r
	
def home(request):
	form = AuthenticationForm()
	context = {
		'patterns': get_all_bracelets(10), 
		'colors': get_colors(),
		'categories': BraceletCategory.objects.all(),
		'loginform':form,
	}
	return render_to_response('bracelet/index.html', context, RequestContext(request))

def add(request):
	context = {'loginform':AuthenticationForm(),
			'colors': get_colors(),
			'categories': BraceletCategory.objects.all(),
			}
	return render_to_response('bracelet/add.html', context, RequestContext(request))

def bracelet(request, bracelet_id):
	bp = BraceletPattern(bracelet_id)
	bp.generate_pattern()
	context = {'loginform':AuthenticationForm(),
			'braceletid':bracelet_id,
			'name' : bp.bracelet.name,
			'style':bp.get_style(),
			'nofstr':bp.get_n_of_strings(),
			'knotsType':bp.get_knots_types(),
			'knotsColor':bp.get_knots_colors(),
			'nofrows':bp.nofrows,
			'bracelet_id':bracelet_id,
			'texts':[str(s) for s in BraceletKnotType.objects.all().order_by('id')],
			}
	
	return render_to_response('bracelet/bracelet.html', context, RequestContext(request))

def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/')

def login_user(request):
	if 'username' in request.POST:
		username = request.POST['username']
		password = request.POST['password']
		form = AuthenticationForm(data=request.POST)
		user = authenticate(username=username, password=password)
		if user is not None and user.is_active:
			login(request, user)
		context = {'loginform':form, 
				'patterns': get_all_bracelets(10), 
				'colors': get_colors(),
				'categories': BraceletCategory.objects.all(),
				}
		return render_to_response('bracelet/index.html', context, RequestContext(request))
	else:
		home(request)

def search(request, page=1):
	# TODO bracelets filter
	context = {'category' : request.GET['category'],
		'difficulty': request.GET['difficulty'],
		'rate': request.GET['rate'],
		'color': request.GET['color'],
		'orderby': request.GET['orderby'],
		'categories': BraceletCategory.objects.all(),
		'photo': 'photo' in request.GET,
		'colors': get_colors(),
		'loginform': AuthenticationForm(),
		'search': True
	}
	context['patterns'] = find_bracelets(category=request.GET['category'], difficulty=request.GET['difficulty'], 
										color=request.GET['color'], orderby=request.GET['orderby'], photo='photo' in request.GET)
	return render_to_response('bracelet/index.html', context, RequestContext(request))

def addpattern(request):
	colors = []
	for c in request.POST:
		if c.find('color')==0:
			colors.append((int('0x'+request.POST[c][1:],16),c[5:]))
	knots = request.POST['pattern'].split()
	b = Bracelet(user = request.user, date = datetime.datetime.today(), name = request.POST['name'], accepted = False, difficulty = request.POST['difficulty'], category = BraceletCategory.objects.filter(name=request.POST['category'])[0])
	b.save()
	for color in colors:
		bs = BraceletString(index=color[1], color=BraceletColor.objects.filter(hexcolor=color[0])[0], bracelet=b)
		bs.save()
	for i in range(len(knots)):
		knotid=0
		if knots[i]=="/":
			knotid=2
		elif knots[i]=="\\":
			knotid=1
		elif knots[i]==">":
			knotid=3
		elif knots[i]=="<":
			knotid=4
		bk =  BraceletKnot(bracelet=b, knottype=BraceletKnotType.objects.filter(id=knotid)[0], index=i)
		bk.save()
	return HttpResponseRedirect('/bracelet/'+str(b.id))
	#return render_to_response('bracelet/index.html', {}, RequestContext(request))

def comments(request, bracelet_id):
	return render_to_response('bracelet/tabs/comments.html', {'comments':'aaaaaa'}, RequestContext(request))

def photos(request, bracelet_id):
	photos = Photo.objects.filter(bracelet = Bracelet.objects.get(id=bracelet_id))
	form = UploadFileForm()
	return render_to_response('bracelet/tabs/photos.html', {'form': form, 'bracelet_id':bracelet_id, 'photos':photos, 'selectTabs':3}, RequestContext(request))

def photo_upload(request, bracelet_id):
	photos = Photo.objects.filter(bracelet = Bracelet.objects.get(id=bracelet_id))
	form = UploadFileForm(request.POST, request.FILES)
	if form.is_valid():
		handle_uploaded_file(request.FILES['file'], request.POST['bracelet_id'], request.user)
		return HttpResponseRedirect('bracelet/'+request.POST['bracelet_id']+'/#ui-tabs-2')
	return render_to_response('bracelet/tabs/photos.html', {'form': form, 'bracelet_id':bracelet_id, 'photos':photos, 'selectTabs':3}, RequestContext(request))



	
