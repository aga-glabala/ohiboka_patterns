from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils import simplejson
from django.utils.safestring import mark_safe
from django.template import Library

register = Library()


def jsonify(obj):
    if isinstance(obj, QuerySet):
        return mark_safe(serialize('json', obj))
    return mark_safe(simplejson.dumps(obj))

register.filter('jsonify', jsonify)
jsonify.is_safe = True
