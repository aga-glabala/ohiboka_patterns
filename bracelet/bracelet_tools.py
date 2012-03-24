'''
Created on Mar 10, 2012

@author: agnis
'''
from bracelet.models import Bracelet, Photo, BraceletCategory, BraceletColor,\
	BraceletString
class BraceletContainer(object):
	def __init__(self, braceletid, author, photo, date, category, colors):
		self.braceletid = braceletid
		self.author = author
		self.photo = photo
		self.date = date
		self.category = category
		self.colors = colors
	def __unicode__(self):
		return "[ id="+self.id+", author="+self.author+", photo="+self.photo+", date="+self.date+", category="+self.category+"]"

def get_all_bracelets(number):
	patterns = Bracelet.objects.all().order_by('-date')
	if number > 0:
		patterns = Bracelet.objects.all().order_by('-date')[:number]
	return create_bracelet_array(patterns)

def find_bracelets(orderby="0", category="0", difficulty="0", color="0", photo=False):
	q_orderby = '-date'
	if orderby=='1':
		q_orderby = 'date'
	#elif request.GET['orderby']=='2':
	#	orderby = '-date'
	#elif request.GET['orderby']=='3':
	#	orderby = '-date'
	patterns = Bracelet.objects.all().order_by(q_orderby)
	if category!="0":
		patterns = patterns.filter(category=BraceletCategory.objects.all().filter(name=category))
	if difficulty!="0":
		patterns = patterns.filter(difficulty=difficulty)		
	# TODO reszta filtrow
	return create_bracelet_array(patterns)

def create_bracelet_array(patterns):
	bracelets = []
	for br in patterns:
		author = br.user.username
		date = br.date.date().__str__()
		photos = Photo.objects.all().filter(bracelet=br)
		print br, photos
		if len(photos)>0 and photos[0].accepted:
			img = photos[0].name
		else:
			img = "nophoto.png"
		colors = []
		cs = BraceletString.objects.filter(bracelet=br)
		for c in cs:
			if not str(c.color) in colors:
				colors.append(str(c.color))
		bracelets.append(BraceletContainer(braceletid=br.id, author=author, photo=img, date=date, category=br.category.id, colors=colors))
	return bracelets

def get_colors():
	colors = []
	for color in BraceletColor.objects.all():
		colors.append(str(color))
	return colors