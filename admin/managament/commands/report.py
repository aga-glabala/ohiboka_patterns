# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from bracelet.models import Bracelet
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.conf import settings
import datetime


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        new_bracelets = Bracelet.objects.waiting().filter(date__gte = datetime.date.today() - \
                                           datetime.timedelta(days = 7))
        subject = '[Ohiboka Patterns] Raport z ' + str(datetime.date.today())
        msg_content = u'Raport z ' + str(datetime.date.today()) + \
            u'\r\n\r\W serwisie jest ' + str(len(new_bracelets)) + u' wzorów do zweryfikowania.' + \
            u'Przejrzyj je tutaj: http://patterns.ohiboka.com/admin/manage_bracelets .'
        for b in new_bracelets:
            msg_content += u'\r\n- ' + b.name + u', dodany ' + str(b.date) + \
                u': http://patterns.ohiboka.com/bracelet/' + b.url
        new_users = User.objects.filter(date_joined__gte = datetime.date.today() - \
                                           datetime.timedelta(days = 7))
        msg_content += u'\r\n\r\nW ciągu ostatniego tygodnia zarejestrowało się ' + \
            str(len(new_users)) + u' nowych użytkowników:'
        for u in new_users:
            msg_content += u'\r\n- ' + u.username + u', zarejestrowany ' + \
                str(u.date_joined) + u': http://patterns.ohiboka.com/user/' + u.username
        msg_content += u'\r\n\r\nhttp://ohiboka.com'

        EmailMessage(subject, msg_content, 'ohiboka@ohiboka.com',
                     [settings.ADMINS[0][1]], headers = {'Reply-To': ['aga@ohiboka.com']}).send()
