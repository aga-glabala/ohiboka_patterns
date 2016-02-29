from django.contrib.auth.models import User
from common.models import UserProfile
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import hashlib
from datetime import date
import logging


class FacebookBackend(ModelBackend):
    """
    Authenticate facebook users
    """

    supports_inactive_user = False

    def authenticate(self, fb_user = None):
        logger = logging.getLogger(__name__)
        try:
            user_profile = UserProfile.objects.get(fb_username = fb_user.id)
            UserModel = get_user_model()
            user = UserModel._default_manager.get_by_natural_key(user_profile.user.username)
            user.backend = 'registration.utils.FacebookBackend'
            return user
        except UserProfile.DoesNotExist:
            # Create a new user. Note that we can set password
            # to anything, because it won't be checked; the password
            # from settings.py will.
            username = fb_user.id
            users = User.objects.filter(username__startswith = username + '-').order_by('id').reverse()
            if not users:
                users = User.objects.filter(username=username).order_by('id').reverse()
                if users:
                    username += '-1'
            else:
                users = users[0]
                username += '-' + str(int(users.url.split('-')[1]) + 1)
            user = User(username=username, password=hashlib.sha224(username + \
                                                str(date.today())).hexdigest())
            user.is_staff = False
            user.is_superuser = False
            user.save()
            userprofile = UserProfile(fb_username = fb_user.id, fb_name = fb_user.name, user = user)
            userprofile.save()
            user.backend = 'common.utils.FacebookBackend'
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
