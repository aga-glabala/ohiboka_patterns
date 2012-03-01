from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.template.context import RequestContext
from bracelet.models import BraceletColor, Bracelet, BraceletCategory,\
	BraceletString, BraceletKnot, BraceletKnotType
from django.forms.models import modelformset_factory
import datetime
from bracelet.Knot import Knot

def home(request):
	form = AuthenticationForm()
	colors = []
	for color in BraceletColor.objects.all():
		colors.append((6-len(hex(color.hexcolor)[2:]))*'0'+hex(color.hexcolor)[2:])
	context = {
		'patterns': ("tmpbracelet.png", "tmpbracelet.png", "tmpbracelet.png", 
				"tmpbracelet.png", "tmpbracelet.png", "tmpbracelet.png", "tmpbracelet.png",
				"tmpbracelet.png", "tmpbracelet.png"), 
		'colors': colors,
		'categories': BraceletCategory.objects.all(),
		'form':form,
	}
	return render_to_response('bracelet/index.html', context, RequestContext(request))

def add(request):
	colors = []
	for color in BraceletColor.objects.all():
		colors.append((6-len(hex(color.hexcolor)[2:]))*'0'+hex(color.hexcolor)[2:])
	context = {'form':AuthenticationForm(),
			'colors': colors,
			'categories': BraceletCategory.objects.all(),}
	return render_to_response('bracelet/add.html', context, RequestContext(request))

def bracelet(request, bracelet_id):
	def calculateColor(knotsType, knotsColor, row, column, last):
		None
		
	def calculateStringsOrder(stringsOrder, knotsType, odd):
		so = []
		if odd==1:
			so.append(stringsOrder[0])
		for i in range(len(knotsType)):
			if knotsType[i] < 3:
				so.append(stringsOrder[i+odd+1])
				so.append(stringsOrder[i+odd])
			elif knotsType[i] > 2:
				so.append(stringsOrder[i+odd])
				so.append(stringsOrder[i+odd+1])
		if odd==1:
			so.append(len(stringsOrder)-1)
	bracelet = Bracelet.objects.get(id=bracelet_id)
	strings = BraceletString.objects.filter(bracelet=bracelet)
	style = ""
	for i in range(len(strings)):
		style+=".str"+str(i)+" {background-color:#"+(6-len(hex(strings[i].color.hexcolor)[2:]))*'0'+hex(strings[i].color.hexcolor)[2:]+";}"
	style+=""
	knotsType = []
	knotsColor = []
	stringsOrder = []
	dbknots = BraceletKnot.objects.filter(bracelet=bracelet)
	
	knotsType[0] = []
	knotsColor[0] = []
	stringsOrder[0] = []
	for i in range(len(strings)/2):
		#color=(6-len(hex(dbknots[i].color.hexcolor)[2:]))*'0'+hex(dbknots[i].color.hexcolor)[2:]
		knotsType[0].append(dbknots[i].knottype.id)
		knotsColor[0].append(i)
	stringsOrder[0] = calculateStringsOrder(range(len(strings)), knotsType[0])

	nofrows = 2*len(dbknots)/(len(strings)-1)
	if(len(dbknots)-nofrows*2*len(dbknots)/(len(strings)-1)>0):
		nofrows+=1
	for row in range(1,nofrows):
		knotsType[row] = []
		knotsColor[row] = []
		for column in range(len(strings)/2 - row%2):
			knotsType[row][column] = dbknots[(len(strings)-1) / 2.0 * row + (row%2)/2.0 + column ].knottype.id
			knotsColor[row][column] = calculateColor(knotsType, knotsColor, row, column, range(len(strings)/2 - row%2))
	context = {'form':AuthenticationForm(),
			'name' : bracelet.name,
			'style':style,
			'nofstr':len(strings),
			'knotsType':knotsType,
			'knotsColor':knotsColor,
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
	context['patterns'] = patterns
	return render_to_response('bracelet/index.html', context, RequestContext(request))

def addpattern(request):
	print request.POST
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
	return render_to_response('bracelet/index.html', {}, RequestContext(request))






