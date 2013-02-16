# -*- coding: utf-8 -*-
'''
Created on Feb 28, 2012

@author: agnis
'''
from bracelet.models import Bracelet, BraceletString, BraceletKnot
import Image, ImageDraw

class BraceletPattern(object):
	'''
	classdocs
	'''

	def __init__(self, bracelet):
		'''
		Constructor
		'''
		self.bracelet = bracelet
		self.strings = BraceletString.objects.filter(bracelet = self.bracelet).order_by('index')
		self.knots = BraceletKnot.objects.filter(bracelet = self.bracelet)
		self.strings_order = [range(len(self.strings))]
		self.odd = len(self.strings) % 2
		self.knots_types = []
		self.knots_colors = []

	def get_style(self):
		style = ""
		for i in range(len(self.strings)):
			style += ".str" + str(i) + " {background-color:" + str(self.strings[i].color) + ";}"
		return style

	def get_colors(self):
		colors = []
		for i in range(len(self.strings)):
			colors.append(str(self.strings[i].color))
		return colors

	def get_ifwhite(self):
		ifwhite = []
		for i in range(len(self.strings)):
			x = str(self.strings[i].color)
			ifwhite.append('-white' if (int(x[1:3], 16) + int(x[3:5], 16) + int(x[5:7], 16)) / 3.0 < 128 else '')
		return ifwhite

	def generate_pattern(self):
		if int(self.bracelet.type) == 1:
			self.nofrows = 2 * len(self.knots) / (len(self.strings) - 1)
			if(len(self.knots) - self.nofrows * (len(self.strings) / 2.0) > 0):
				self.nofrows += 1
			nofcols = len(self.strings) / 2
			types = []
			colors = []
			for i in range(nofcols):
				types.append(int(self.knots[i].knottype.id))
			self.knots_types.append(types)
			for i in range(nofcols):
				colors.append(self.get_knot_color(self.strings_order[0], self.knots_types[0], i, 0))
			self.knots_colors.append(colors)
			index = nofcols
			for i in range(1, self.nofrows):
				self.strings_order.append(self.get_next_strings_order(self.strings_order[i - 1], self.knots_types[i - 1], (i - 1) % 2))
				colors = []
				types = []
				if self.odd == 0:
					noc = nofcols - (i % 2) # dla parzystej liczby nitek 
				else:
					noc = nofcols

				for j in range(noc):
					types.append(int(self.knots[index].knottype.id))
					index += 1
				self.knots_types.append(types)
				for j in range(noc):
					colors.append(self.get_knot_color(self.strings_order[i], self.knots_types[i], j, i % 2))
				self.knots_colors.append(colors)
			#last row of strings
			self.strings_order.append(self.get_next_strings_order(self.strings_order[self.nofrows - 1], self.knots_types[self.nofrows - 1], (self.nofrows - 1) % 2))
			if self.odd == 0:
				noc = nofcols - (i % 2) # dla parzystej liczby nitek 
			else:
				noc = nofcols
			colors = []
			for j in range(noc):
				colors.append(self.get_knot_color(self.strings_order[self.nofrows - 1], self.knots_types[self.nofrows - 1], j, (self.nofrows - 1) % 2))
			self.knots_colors.append(colors)
		elif int(self.bracelet.type) == 2:
			self.nofrows = (len(self.knots) + 1) / (len(self.strings) - 1)
			nofcols = len(self.strings) - 1
			for i in range(self.nofrows):
				types = []
				colors = []
				for j in range(nofcols):
					knotType = int(self.knots[i * nofcols + j].knottype.id)
					types.append(knotType)
					colors.append(0 if knotType == 5 else j + 1)
				self.knots_types.append(types)
				self.knots_colors.append(colors)

	def get_next_strings_order(self, strings_order, knots_type, odd):
		so = []
		if odd == 1:
			so.append(strings_order[0])
		for i in range(len(knots_type)):
			if knots_type[i] < 3:
				so.append(strings_order[2 * i + odd + 1])
				so.append(strings_order[2 * i + odd])
			elif knots_type[i] > 2:
				so.append(strings_order[2 * i + odd])
				so.append(strings_order[2 * i + odd + 1])
		if self.odd and odd == 0:
			so.append(strings_order[-1])
		elif odd == 1and not self.odd:
			so.append(strings_order[-1])
		return so

	def get_knot_color(self, strings_order, knots_type, column, odd):
		if odd == 1:
			left_color = strings_order[column * 2 + 1]
			right_color = strings_order[column * 2 + 2]
		else:
			left_color = strings_order[column * 2]
			right_color = strings_order[column * 2 + 1]
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

	def generate_photo(self, path):
		if int(self.bracelet.type) == 1:
			im = Image.new(mode = "RGB", size = (self.nofrows * 100 + 16, len(self.strings) / 2 * 160 + 16 + 36), color = "#fff")
			draw = ImageDraw.Draw(im)

			for i in range(self.nofrows):
				if i % 2 == 0 and self.odd or i % 2 == 1 and not self.odd:
					marginTop = 80
				else:
					marginTop = 0
				for j in range(len(self.knots_colors[i])):
					color = str(self.strings[self.knots_colors[i][len(self.knots_colors[i]) - 1 - j]].color)
					x = 8 + i * 100
					y = 8 + j * 160 + marginTop
					draw.ellipse((x - 8, y - 8, x + 116, y + 116), fill = 0x666666)
					draw.ellipse((x - 4, y - 4, x + 108, y + 108), fill = color)
			im = im.resize((self.nofrows * 10 + 1, len(self.strings) / 2 * 16 + 4), Image.ANTIALIAS)
		if int(self.bracelet.type) == 2:
			im = Image.new(mode = "RGB", size = (self.nofrows * 100 + 16, len(self.strings) * 100 + 16), color = "#fff")
			draw = ImageDraw.Draw(im)

			for i in range(self.nofrows):
				for j in range(len(self.knots_colors[i])):
					color = str(self.strings[self.knots_colors[i][len(self.knots_colors[i]) - 1 - j]].color)
					x = 8 + i * 100
					y = 8 + j * 100
					draw.ellipse((x - 8, y - 8, x + 108, y + 108), fill = 0x666666)
					draw.ellipse((x - 4, y - 4, x + 104, y + 104), fill = color)
			im = im.resize((self.nofrows * 10 + 1, len(self.strings) * 10 + 1), Image.ANTIALIAS)
		im.save(path)

def get_custom_characters():
	characters = [" ", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H",
				  "I", "J", "K", "L", "M", "N", "O", "P", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a",
				  "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t",
				  "u", "v", "w", "x", "y", "z", "!", "#", "^", "*", "(", ")", ":", "'", "\"", "<", ">", "?", "/", "\\",
				  "|", "+", "-", "=", "_", "*", "⁙", "‹", "›", "↓", "←", "↑", "→", "◆", "◇", "▲", "△", "♥"]
	return characters
