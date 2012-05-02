from django.contrib.auth.models import User
from registration.models import UserProfile
import hashlib
from django.contrib.auth.backends import ModelBackend

class FacebookBackend(ModelBackend):
	"""
	Authenticate facebook users
	"""

	supports_inactive_user = False

	def authenticate(self, fb_user=None):
		try:
			user_profile = UserProfile.objects.get(fb_username=fb_user.username)
			user_profile.user.backend = 'ohibokapatterns.registration.utils.FacebookBackend'
			return user_profile.user
		except UserProfile.DoesNotExist:
			# Create a new user. Note that we can set password
			# to anything, because it won't be checked; the password
			# from settings.py will.
			username = hashlib.sha224(fb_user.username+fb_user.name).hexdigest()
			user = User(username=username, password='')
			user.is_staff = False
			user.is_superuser = False
			user.save()
			userprofile = UserProfile(fb_username = fb_user.username, fb_name = fb_user.name, user = user)
			userprofile.save()
			user.backend = 'ohibokapatterns.registration.utils.FacebookBackend'
			return user
		
	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None