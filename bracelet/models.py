from django.db import models
from django.contrib.auth.models import User

class BraceletCategory(models.Model):
	name = models.CharField(max_length=50)
	def __unicode__(self):
		return self.name
	
class Bracelet(models.Model):
	user = models.ForeignKey(User, related_name='+')
	date = models.DateTimeField('Creation date')
	name = models.CharField(max_length=50)
	accepted = models.BooleanField()
	difficulty = models.IntegerField(choices=((0, ' Easy'), (1, 'Medium'), (2, 'Hard')))
	category = models.ForeignKey(BraceletCategory, related_name='+')
	def __unicode__(self):
		return "[id="+str(self.id)+", user="+str(self.user)+", name="+self.name+", accepted="+str(self.accepted)+", difficulty="+str(self.difficulty)+", category="+str(self.category)+"]"
	
class BraceletColor(models.Model):
	hexcolor = models.IntegerField()
	def __unicode__(self):
		return "#"+(6-len(hex(self.hexcolor)[2:]))*'0'+hex(self.hexcolor)[2:]
	
class BraceletString(models.Model):
	index = models.IntegerField()
	color = models.ForeignKey(BraceletColor, related_name='+')
	bracelet = models.ForeignKey(Bracelet, related_name='+')
	def __unicode__(self):
		return "[id="+str(self.id)+", index="+str(self.index)+", color="+str(self.color)+"]"

class BraceletKnotType(models.Model):
	text = models.CharField(max_length=100)
	def __unicode__(self):
		return self.text
	
class BraceletKnot(models.Model):
	index = models.IntegerField()
	bracelet = models.ForeignKey(Bracelet, related_name='+')
	knottype = models.ForeignKey(BraceletKnotType, related_name='+')
	def __unicode__(self):
		return "[id="+str(self.id)+", index="+str(self.index)+", knottype="+str(self.knottype.id)+", bracelet="+str(self.bracelet.id)+"]"
	
class Photo(models.Model):
	name = models.CharField(max_length=50)
	accepted = models.BooleanField()
	bracelet = models.ForeignKey(Bracelet, related_name='+')
	user = models.ForeignKey(User, related_name='+')
	def __unicode__(self):
		return "[id="+str(self.id)+", accepted="+str(self.accepted)+", bracelet="+str(self.bracelet.id)+", user="+self.user.username+"]"
	
	
	