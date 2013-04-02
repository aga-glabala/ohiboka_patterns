'''
Created on Jul 28, 2012

@author: agnis
'''
from bracelet.models import Bracelet
from common.views import get_context, index
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext as _


def manage_bracelets(request, context_={}):
    if request.user.is_staff:
        bracelets = Bracelet.objects.all()
        accepted = []
        rejected = []
        to_accept = []
        for b in bracelets:
            if b.accepted == -1:
                rejected.append(b)
            elif b.accepted == 0:
                to_accept.append(b)
            elif b.accepted == 1:
                accepted.append(b)
        context = get_context(request)
        context.update(context_)
        context['accepted'] = accepted
        context['rejected'] = rejected
        context['to_accept'] = to_accept
        return render_to_response('admin/manage_bracelets.html', context, RequestContext(request))
    return index(request, {'error_message': _('You have no permission to see this')})
