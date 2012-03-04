from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.template.context import RequestContext
from bracelet.models import BraceletColor, Bracelet, BraceletCategory,\
	BraceletString, BraceletKnot, BraceletKnotType, Photo
import datetime
from bracelet.pattern_tools import BraceletPattern, BraceletContainer

def setlang(request, lang):
	request.session['django_language'] = lang
	r = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	r.set_cookie('django_language', lang)
	return r
	
def home(request):
	form = AuthenticationForm()
	colors = []
	for color in BraceletColor.objects.all():
		colors.append(str(color))
	bracelets = Bracelet.objects.all().order_by('-date')[:10]
	imgs = []
	for br in bracelets:
		author = br.user.username
		date = br.date.date().__str__()
		photos = Photo.objects.all().filter(bracelet=br)
		if len(photos)>0 and photos[0].accepted:
			img = str(photos[0].id)+".png" 
		else:
			img = "nophoto.png"
		imgs.append(BraceletContainer(id=br.id, author=author, photo=img, date=date))
	context = {
		'patterns': imgs, 
		'colors': colors,
		'categories': BraceletCategory.objects.all(),
		'form':form,
	}
	return render_to_response('bracelet/index.html', context, RequestContext(request))

def add(request):
	colors = []
	for color in BraceletColor.objects.all():
		colors.append(str(color.hexcolor))
	context = {'form':AuthenticationForm(),
			'colors': colors,
			'categories': BraceletCategory.objects.all(),
			}
	return render_to_response('bracelet/add.html', context, RequestContext(request))

def bracelet(request, bracelet_id):
	bp = BraceletPattern(bracelet_id)
	bp.generate_pattern()
	context = {'form':AuthenticationForm(),
			'name' : bp.bracelet.name,
			'style':bp.get_style(),
			'nofstr':bp.get_n_of_strings(),
			'knotsType':bp.get_knots_types(),
			'knotsColor':bp.get_knots_colors(),
			'nofrows':bp.nofrows,
			'bracelet_id':bracelet_id,
			}
	
	return render_to_response('bracelet/bracelet.html', context, RequestContext(request))

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
			# TODO Redirect to a success page.
			print "1"
		else:
			# TODO Return a 'disabled account' error message
			print "2"
	else:
		# TODO Return an 'invalid login' error message.
		print "3"
	return HttpResponseRedirect('/')


def search(request, page=1):
	colors = []
	for color in BraceletColor.objects.all():
		colors.append((6-len(hex(color.hexcolor)[2:]))*'0'+hex(color.hexcolor)[2:])
	# TODO bracelets filter
	context = {'category' : request.GET['category'],
		'difficulty': request.GET['difficulty'],
		'rate': request.GET['rate'],
		'color': request.GET['color'],
		'orderby': request.GET['orderby'],
		'categories': BraceletCategory.objects.all(),
		'photo': 'photo' in request.GET,
		'colors': colors,
		'form': AuthenticationForm(),
		'search': True
	}
	orderby = 'date'
	if request.GET['orderby']=='1':
		orderby = '-date'
	#elif request.GET['orderby']=='2':
	#	orderby = '-date'
	#elif request.GET['orderby']=='3':
	#	orderby = '-date'
	patterns = Bracelet.objects.all().order_by(orderby)
	if request.GET['category']!="0":
		patterns = patterns.filter(category=BraceletCategory.objects.all().filter(name=request.GET['category']))
	if request.GET['difficulty']!="0":
		patterns = patterns.filter(difficulty=request.GET['difficulty'])
		# TODO reszta filtrow
	bracelets = []
	for br in patterns:
		author = br.user.username
		date = br.date.date().__str__()
		photos = Photo.objects.all().filter(bracelet=br)
		if len(photos)>0 and photos[0].accepted:
			img = str(photos[0].id)+".png" 
		else:
			img = "nophoto.png"
		bracelets.append(BraceletContainer(id=br.id, author=author, photo=img, date=date))
	context['patterns'] = bracelets
	print bracelets
	return render_to_response('bracelet/index.html', context, RequestContext(request))

def addpattern(request):
	colors = []
	for c in request.POST:
		if c.find('color')==0:
			colors.append((int('0x'+request.POST[c],16),c[5:]))
	knots = request.POST['pattern'].split()
	b = Bracelet(user = request.user, date = datetime.datetime.today(), name = request.POST['name'], accepted = False, difficulty = request.POST['difficulty'], category = BraceletCategory.objects.filter(name=request.POST['category'])[0])
	b.save()
	for color in colors:
		bs = BraceletString(index=color[1], color=BraceletColor.objects.filter(hexcolor=color[0])[0], bracelet=b)
		bs.save()
	for i in range(len(knots)):
		id=0
		if knots[i]=="/":
			id=2
		elif knots[i]=="\\":
			id=1
		elif knots[i]==">":
			id=3
		elif knots[i]=="<":
			id=4
		bk =  BraceletKnot(bracelet=b, knottype=BraceletKnotType.objects.filter(id=id)[0], index=i)
		bk.save()
	return HttpResponseRedirect('/bracelet/'+str(b.id))
	#return render_to_response('bracelet/index.html', {}, RequestContext(request))

def comments(request, bracelet_id):
	return render_to_response('bracelet/tabs/comments.html', {'comments':'aaaaaa'}, RequestContext(request))




