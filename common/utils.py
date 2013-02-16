from django.contrib.auth.models import User
from common.models import UserProfile
from django.contrib.auth.backends import ModelBackend
import hashlib
from datetime import date

class FacebookBackend(ModelBackend):
    """
    Authenticate facebook users
    """

    supports_inactive_user = False

    def authenticate(self, fb_user = None):
        try:
            user_profile = UserProfile.objects.get(fb_username = fb_user.username)
            user_profile.user.backend = 'ohibokapatterns.common.utils.FacebookBackend'
            return user_profile.user
        except UserProfile.DoesNotExist:
            # Create a new user. Note that we can set password
            # to anything, because it won't be checked; the password
            # from settings.py will.
            username = fb_user.username
            users = User.objects.filter(username__startswith = username + '-').order_by('id').reverse()
            if not users:
                users = User.objects.filter(username = username).order_by('id').reverse()
                if users:
                    username += '-1'
            else:
                users = users[0]
                username += '-' + str(int(users.url.split('-')[1]) + 1)
            user = User(username = username, password = hashlib.sha224(username + str(date.today())).hexdigest())
            user.is_staff = False
            user.is_superuser = False
            user.save()
            userprofile = UserProfile(fb_username = fb_user.username, fb_name = fb_user.name, user = user)
            userprofile.save()
            user.backend = 'ohibokapatterns.common.utils.FacebookBackend'
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk = user_id)
        except User.DoesNotExist:
            return None
