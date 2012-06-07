'''
Created on Mar 15, 2012

@author: agnis
'''

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	fb_username = models.CharField(max_length=100)
	fb_name = models.CharField(max_length=100)