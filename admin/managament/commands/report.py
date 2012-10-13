# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from bracelet.models import Bracelet
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.conf import settings
import datetime

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		nowe_bracelety = Bracelet.objects.filter(accepted = 0)
		subject = 'Your bracelet was accepted | Twoja bransoletka została zaakceptowana'
		msg_content = u'Cześć (witam samą siebie - 4ever alone)!'+\
			u'\r\nW ciągu ostatniego tygodnia pojawiło się '+str(len(nowe_bracelety))+u' nowych wzorów.'+\
			u'Przejrzyj je tutaj: http://patterns.ohiboka.com/admin/manage_bracelets .'
		for b in nowe_bracelety:
			msg_content += u'\r\n- '+b.name+ u', dodany '+str(b.date)+ u': http://patterns.ohiboka.com/bracelet/'+b.url
		nowi_juzerzy = User.objects.filter(date_joined__gte = datetime.date.today() - datetime.timedelta(days = 7))
		msg_content += u'\r\n\r\nZarejestrowało się '+str(len(nowi_juzerzy))+u' nowych użytkowników:'
		for u in nowi_juzerzy:
			msg_content += u'\r\n- '+u.username+ u', zarejestrowany '+str(u.date_joined)+ u': http://patterns.ohiboka.com/user/'+u.username
		msg_content += u'\r\n\r\nhttp://ohiboka.com'
						
		EmailMessage(subject, msg_content, 'ohiboka@ohiboka.com', [settings.ADMINS[0][1]], headers = {'Reply-To': ['aga@ohiboka.com']}).send()