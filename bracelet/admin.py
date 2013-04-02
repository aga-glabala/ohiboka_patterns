from django.contrib import admin
from bracelet.models import BraceletCategory
from bracelet.models import Bracelet
from bracelet.models import BraceletColor
from bracelet.models import BraceletString
from bracelet.models import Photo

admin.site.register(BraceletCategory)
admin.site.register(Bracelet)
admin.site.register(BraceletColor)
admin.site.register(BraceletString)
admin.site.register(Photo)
