'''
Created on Feb 28, 2012

@author: agnis
'''
from bracelet.models import Bracelet, BraceletString, BraceletKnot

class BraceletPattern(object):
	'''
	classdocs
	'''

	def __init__(self, bracelet_id):
		'''
		Constructor
		'''
		self.bracelet = Bracelet.objects.get(id=bracelet_id)
		self.strings = BraceletString.objects.filter(bracelet=self.bracelet).order_by('index')
		self.knots = BraceletKnot.objects.filter(bracelet=self.bracelet)
		self.strings_order = [range(len(self.strings))]
		self.odd = len(self.strings)%2
		self.knots_types = []
		self.knots_colors = []
		
	def get_style(self):
		style = ""
		for i in range(len(self.strings)):
			style+=".str"+str(i)+" {background-color:"+str(self.strings[i].color)+";}"
		return style
	
	def generate_pattern(self):
		self.nofrows = 2*len(self.knots)/(len(self.strings)-1)
		if(len(self.knots)-self.nofrows*(len(self.strings)/2.0)>0):
			self.nofrows+=1
		nofcols = len(self.strings)/2
		types = []
		colors = []
		for i in range(nofcols):
			types.append(self.knots[i].knottype.id)
		self.knots_types.append(types)
		for i in range(nofcols):
			colors.append(self.get_knot_color(self.strings_order[0], self.knots_types[0], i, 0))
		self.knots_colors.append(colors)
		index = nofcols
		for i in range(1, self.nofrows):
			self.strings_order.append(self.get_next_strings_order(self.strings_order[i-1], self.knots_types[i-1], (i-1)%2))
			colors = []
			types = []
			if self.odd == 0:
				noc = nofcols-(i%2) # dla parzystej liczby nitek 
			else:
				noc = nofcols
			
			for j in range(noc):
				types.append(self.knots[index].knottype.id)
				index+=1
			self.knots_types.append(types)	
			for j in range(noc):
				colors.append(self.get_knot_color(self.strings_order[i], self.knots_types[i], j, i%2))
			self.knots_colors.append(colors)
		
	def get_next_strings_order(self, strings_order, knots_type, odd):	
		so = []
		if odd==1:
			so.append(strings_order[0])
		for i in range(len(knots_type)):
			if knots_type[i] < 3:
				so.append(strings_order[2*i+odd+1])
				so.append(strings_order[2*i+odd])
			elif knots_type[i] > 2:
				so.append(strings_order[2*i+odd])
				so.append(strings_order[2*i+odd+1])
		if self.odd and odd==0:
			so.append(strings_order[-1])
		elif odd==1and not self.odd:
			so.append(strings_order[-1])
		return so
	
	def get_knot_color(self, strings_order, knots_type, column, odd):
		if odd==1:
			left_color = strings_order[column*2+1]
			right_color = strings_order[column*2+2]
		else: 
			left_color = strings_order[column*2]
			right_color = strings_order[column*2+1]
		if knots_type[column] == 1 or knots_type[column] == 3:
			return left_color
		elif knots_type[column] == 2 or knots_type[column] == 4:
			return right_color
		return -1
	
	def get_strings(self):
		return self.strings_order
	
	def get_n_of_strings(self):
		return len(self.strings)
	
	def get_knots_colors(self):
		return self.knots_colors
	
	def get_knots_types(self):
		return self.knots_types
	
