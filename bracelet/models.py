from django.db import models
from django.contrib.auth.models import User

class BraceletCategory(models.Model):
	name = models.CharField(max_length = 50)
	def __unicode__(self):
		return self.name

class Bracelet(models.Model):
	user = models.ForeignKey(User, related_name = 'bracelets')
	photo = models.ForeignKey('Photo', related_name = '+', default = '')
	date = models.DateTimeField('Creation date')
	name = models.CharField(max_length = 50)
	accepted = models.IntegerField(default = 0)
	difficulty = models.IntegerField(choices = ((0, ' Easy'), (1, 'Medium'), (2, 'Hard')))
	category = models.ForeignKey(BraceletCategory, related_name = 'bracelets')
	rate = models.DecimalField(max_digits = 3, decimal_places = 2)
	public = models.BooleanField(default = False)
	url = models.CharField(max_length = 52, unique = True, null = False)
	deleted = models.BooleanField(default = False)

	def __unicode__(self):
		return "[id=" + str(self.id) + ", user=" + str(self.user) + ", name=" + self.name + ", accepted=" + str(self.accepted) + ", difficulty=" + str(self.difficulty) + ", category=" + str(self.category) + "]"

	def get_average_rate(self):
		rate = 0
		rates = self.rates.all()
		if not rates:
			return 0
		for r in rates:
			rate += r.rate
		return rate * 1.0 / len(rates)

class BraceletColor(models.Model):
	hexcolor = models.IntegerField()
	def __unicode__(self):
		return "#" + (6 - len(hex(int(self.hexcolor))[2:])) * '0' + hex(int(self.hexcolor))[2:]

class BraceletString(models.Model):
	index = models.IntegerField()
	color = models.ForeignKey(BraceletColor, related_name = 'bracelets')
	bracelet = models.ForeignKey(Bracelet, related_name = 'strings')
	def __unicode__(self):
		return "[id=" + str(self.id) + ", index=" + str(self.index) + ", color=" + str(self.color) + "]"

class BraceletKnotType(models.Model):
	text = models.CharField(max_length = 100)
	def __unicode__(self):
		return self.text

class BraceletKnot(models.Model):
	index = models.IntegerField()
	bracelet = models.ForeignKey(Bracelet, related_name = 'knots')
	knottype = models.ForeignKey(BraceletKnotType, related_name = '+')
	def __unicode__(self):
		return "[id=" + str(self.id) + ", index=" + str(self.index) + ", knottype=" + str(self.knottype.id) + ", bracelet=" + str(self.bracelet.id) + "]"

class Photo(models.Model):
	name = models.CharField(max_length = 50)
	accepted = models.BooleanField(default = False)
	bracelet = models.ForeignKey(Bracelet, related_name = 'photos')
	user = models.ForeignKey(User, related_name = 'photos')
	def __unicode__(self):
		return "[id=" + str(self.id) + ", accepted=" + str(self.accepted) + ", bracelet=" + str(self.bracelet.id) + ", user=" + self.user.username + "]"

class Rate(models.Model):
	bracelet = models.ForeignKey(Bracelet, related_name = 'rates')
	rate = models.IntegerField()
	user = models.ForeignKey(User, related_name = 'rates')
