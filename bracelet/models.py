from django.db import models
from django.contrib.auth.models import User

class BraceletCategory(models.Model):
    name = models.CharField(max_length=50)
        
class Bracelet(models.Model):
    user = models.ForeignKey(User, related_name='+')
    date = models.DateTimeField('Creation date')
    name = models.CharField(max_length=50)
    accepted = models.BooleanField()
    difficulty = models.IntegerField(choices=((0, ' Easy'), (1, 'Medium'), (2, 'Hard')))
    category = models.ForeignKey(BraceletCategory, related_name='+')
    
class BraceletColor(models.Model):
    hexcolor = models.IntegerField()
    
class BraceletString(models.Model):
    index = models.IntegerField()
    color = models.ForeignKey(BraceletColor, related_name='+')
    bracelet = models.ForeignKey(Bracelet, related_name='+')

class BraceletKnotType(models.Model):
    text = models.CharField(max_length=100)
    
class BraceletKnot(models.Model):
    index = models.IntegerField()
    bracelet = models.ForeignKey(Bracelet, related_name='+')
    knottype = models.ForeignKey(BraceletKnotType, related_name='+')
    
class Photo(models.Model):
    name = models.CharField(max_length=50)
    accepted = models.BooleanField()
    bracelet = models.ForeignKey(Bracelet, related_name='+')
    user = models.ForeignKey(User, related_name='+')
    