'''
Created on Jul 28, 2012

@author: agnis
'''
from bracelet.models import Bracelet
from common.views import get_context
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect
from django.contrib import messages


def manage_bracelets(request, context_ = {}):
    if request.user.is_staff:
        context = get_context(request)
        context.update(context_)
        context['accepted'] = Bracelet.objects.accepted()
        context['rejected'] = Bracelet.objects.rejected()
        context['to_accept'] = Bracelet.objects.waiting()
        return render_to_response('admin/manage_bracelets.html', context, RequestContext(request))
    messages.error(request, _('You have no permission to see this'))
    return HttpResponseRedirect('/')
