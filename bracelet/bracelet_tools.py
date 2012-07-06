'''
Created on Mar 10, 2012

@author: agnis
'''
from bracelet.models import Bracelet, Photo, BraceletCategory, BraceletColor,\
	BraceletString, Rate
from datetime import datetime
from django.db.models.aggregates import Avg
class BraceletContainer(object):
	def __init__(self, braceletid, name, author, photo, now, category, colors, average_rate, nofstrings, difficulty, date, nofvotes):
		self.braceletid = braceletid
		self.name = name
		self.author = author
		self.photo = photo
		self.now = now
		self.category = category
		self.colors = colors
		self.nofstrings = nofstrings
		self.difficulty = difficulty
		self.date = date
		self.nofvotes = nofvotes
		self.average_rate = average_rate
	def __unicode__(self):
		return "[ author="+str(self.author)+", photo="+str(self.photo)+", date="+str(self.date)+", category="+str(self.category)+"]"

def get_all_bracelets(number, user=None):
	patterns = None
	if user:
		patterns = Bracelet.objects.filter(user=user).order_by('-date')
	else:
		patterns = Bracelet.objects.all().order_by('-date')
	if number > 0:
		patterns = patterns[:number]
	return create_bracelet_array(patterns)

def find_bracelets(orderby="0", category="0", difficulty="0", color="0", photo=False, rate="0"):
	q_orderby = '-date'
	if orderby=='1':
		q_orderby = 'date'
	elif orderby=='2':
		q_orderby = '-rate'
	elif orderby=='3':
		q_orderby = 'rate'
	patterns = Bracelet.objects.all().order_by(q_orderby)
	if category!="0":
		patterns = patterns.filter(category=BraceletCategory.objects.all().filter(name=category))
	if difficulty!="0":
		patterns = patterns.filter(difficulty=difficulty)
	
	rate = int(rate)
	if	rate>0:
		patterns = patterns.filter(rate__gte = rate) 
	if photo:	
		patterns = patterns.filter(photo__isnull=False)
		
	if color:
		color = BraceletColor.objects.get(hexcolor = int('0x'+color[1:],16))
		strings = [bs.bracelet.id for bs in BraceletString.objects.filter(color = color)] # TODO find more effective way to do this
		patterns = patterns.filter(id__in = strings)

	return create_bracelet_array(patterns)

def create_bracelet_array(patterns):
	bracelets = []
	for br in patterns:
		author = br.user.username
		d = datetime.now() - br.date
		now  = d.days < 7 
		photos = Photo.objects.all().filter(bracelet=br)
		if len(photos)>0 and photos[0].accepted:
			img = photos[0].name
		else:
			img = "nophoto.png"
		colors = []
		cs = BraceletString.objects.filter(bracelet=br)
		for c in cs:
			if not str(c.color) in colors:
				colors.append(str(c.color))
		nofvotes = len(Rate.objects.filter(bracelet = br))
		bracelets.append(BraceletContainer(braceletid=br.id, name=br.name, author=author, photo=img, now = now, 
										   category=br.category.id, colors=colors, nofstrings = len(colors), 
										   average_rate = br.rate, difficulty = br.difficulty, date = br.date.date().__str__(), nofvotes = nofvotes))
	return bracelets

def get_colors():
	colors = []
	for color in BraceletColor.objects.all():
		colors.append(str(color))
	return colors