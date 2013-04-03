'''
Created on Mar 10, 2012

@author: agnis
'''
from bracelet.models import Bracelet, BraceletCategory, BraceletColor, \
    BraceletString, Rate
from datetime import datetime


class BraceletContainer(Bracelet):
    def __init__(self, bracelet, now, colors, nofstrings, nofvotes):
        self.__dict__ = bracelet.__dict__.copy()
        # self.bracelet = bracelet
        self.now = now
        self.colors = colors
        self.nofstrings = nofstrings
        self.date = bracelet.date.date().__str__()
        self.nofvotes = nofvotes
        self.short_rate = int(bracelet.rate)

    def __unicode__(self):
        return "[author=" + str(self.author) + ", photo=" + str(self.photo) + \
               ", date=" + str(self.date) + ", category=" + str(self.category)\
               + "]"


def get_all_bracelets(number, user=None, accepted=True):

    patterns = Bracelet.objects.order_by('-date')
    if user:
        patterns = patterns.filter(user=user)

    if accepted:
        patterns = patterns.filter(accepted=True, deleted=False)
    else:
        patterns = patterns.filter(deleted=False)
    if number > 0:
        patterns = patterns[:number]
    return create_bracelet_array(patterns)


def find_bracelets(orderby="0", category="0", difficulty="0", color="0",
                   photo=False, rate="0"):
    q_orderby = '-date'
    if orderby == '1':
        q_orderby = 'date'
    elif orderby == '2':
        q_orderby = '-rate'
    elif orderby == '3':
        q_orderby = 'rate'
    patterns = Bracelet.objects.accepted().order_by(q_orderby)
    if category != "0":
        patterns = patterns.filter(category=BraceletCategory.objects.filter(name=category))
    if difficulty != "0":
        patterns = patterns.filter(difficulty=difficulty)

    rate = int(rate)
    if rate > 0:
        patterns = patterns.filter(rate__gte=int(rate))

    if photo:
        for pattern in patterns:
            print pattern, pattern.photos.filter(accepted=1).all()
            if len(pattern.photos.all()) < 1:
                del pattern

    if color != "0":
        color = BraceletColor.objects.get(hexcolor=int('0x' + color[1:], 16))
        strings = [bs.bracelet.id for bs in BraceletString.objects.filter(color=color)]
        patterns = patterns.filter(id__in=strings)

    return create_bracelet_array(patterns)


def create_bracelet_array(patterns):
    bracelets = []
    for br in patterns:
        d = datetime.now() - br.date
        now = d.days < 7

        colors = []
        cs = BraceletString.objects.filter(bracelet=br)
        for c in cs:
            if not str(c.color) in colors:
                colors.append(str(c.color))
        nofvotes = len(Rate.objects.filter(bracelet=br))
        bracelets.append(BraceletContainer(bracelet=br, now=now, colors=colors,
                        nofstrings=len(colors), nofvotes=nofvotes))
    return bracelets


def get_colors():
    colors = []
    for color in BraceletColor.objects.all():
        colors.append(str(color))
    return colors
