import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.query import QuerySet


class BraceletCategory(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class BraceletQuerySet(QuerySet):

    def accepted(self, user=None):
        """Filter out bracelets that are published"""
        if user:
            return self.filter(accepted=1, public=1, deleted=False, user=user)
        else:
            return self.filter(accepted=1, public=1, deleted=False)

    def waiting(self, user=None):
        """Filter out bracelets that are waiting for acceptance"""
        if user:
            return self.filter(accepted=0, public=1, deleted=False, user=user)
        else:
            return self.filter(accepted=0, public=1, deleted=False)

    def rejected(self, user=None):
        """Filter out bracelets that are rejected"""
        if user:
            return self.filter(accepted= -1, public=1, deleted=False, user=user)
        else:
            return self.filter(accepted= -1, public=1, deleted=False)

    def private(self, user=None):
        """Filter out bracelets that are private"""
        if user:
            return self.filter(public=0, user=user)
        else:
            return self.filter(public=0)

    def find_bracelets(self, orderby="0", category="0", difficulty="0", color="0", photo=False, rate="0"):
        q_orderby = '-date'
        if orderby == '1':
            q_orderby = 'date'
        elif orderby == '2':
            q_orderby = '-rate'
        elif orderby == '3':
            q_orderby = 'rate'
        patterns = self.accepted().order_by(q_orderby)
        if category != "0":
            patterns = patterns.filter(category=BraceletCategory.objects.filter(name=category))
        if difficulty != "0":
            patterns = patterns.filter(difficulty=difficulty)

        rate = int(rate)
        if rate > 0:
            patterns = patterns.filter(rate__gte=rate)

        if photo:
            for pattern in patterns:
                # since we always have picture of pattern we need at least two photos in database
                if len(pattern.photos.all()) < 2:
                    del pattern

        if color != "0":
            color = BraceletColor.objects.get(hexcolor=int('0x' + color[1:], 16))
            #strings = [bs.bracelet.id for bs in BraceletString.objects.filter(color=color)]
            patterns = patterns.filter(colors__contains=color)

        return patterns


class BraceletManager(models.Manager):
    def get_query_set(self):
        return BraceletQuerySet(self.model)
    def __getattr__(self, attr, *args):
        # see https://code.djangoproject.com/ticket/15062 for details
        if attr.startswith("_"):
            raise AttributeError
        return getattr(self.get_query_set(), attr, *args)

class Bracelet(models.Model):
    objects = BraceletManager()
    user = models.ForeignKey(User, related_name='bracelets')
    photo = models.ForeignKey('Photo', related_name='photos', default='')
    date = models.DateTimeField('Creation date')
    name = models.CharField(max_length=50)
    accepted = models.IntegerField(default=0)
    difficulty = models.IntegerField(choices=((1, ' Easy'), (2, 'Medium'), (3, 'Hard')))
    category = models.ForeignKey(BraceletCategory, related_name='bracelets')
    rate = models.DecimalField(max_digits=3, decimal_places=2)
    public = models.BooleanField(default=False)
    url = models.CharField(max_length=52, unique=True, null=False)
    deleted = models.BooleanField(default=False)
    type = models.IntegerField(choices=((1, 'Diagonal'), (2, 'Straight')))

    def __unicode__(self):
        return "[id=" + str(self.id) + ", user=" + str(self.user) + ", name="\
            + self.name + ", accepted=" + str(self.accepted)\
            + ", difficulty=" + str(self.difficulty) + ", category="\
            + str(self.category) + ", rate=" + str(self.rate)\
            + ", public=" + str(self.public) + ", type = " \
            + str(self.type) + "]"

    def get_average_rate(self):
        rate = 0
        rates = self.rates.all()
        if not rates:
            return 0
        for r in rates:
            rate += r.rate
        return rate * 1.0 / len(rates)

    @property
    def new(self):
        d = datetime.datetime.now() - self.date
        return d.days < 7

    @property
    def nofstrings(self):
        return len(self.colors)

    @property
    def nofvotes(self):
        return len(self.rates)

    @property
    def unique_colors(self):
        colors = []
        for color in self.colors:
            colors.append(str(color))

class BraceletColorQuerySet(QuerySet):
    def all_hexes(self):
        colors = []
        for color in self.all():
            if not str(color) in colors:
                colors.append(str(color))
        return colors


class BraceletColorManager(models.Manager):
    def get_query_set(self):
        return BraceletColorQuerySet(self.model)
    def __getattr__(self, attr, *args):
        # see https://code.djangoproject.com/ticket/15062 for details
        if attr.startswith("_"):
            raise AttributeError
        return getattr(self.get_query_set(), attr, *args)


class BraceletColor(models.Model):
    objects = BraceletColorManager()
    hexcolor = models.IntegerField()

    def __unicode__(self):
        return "#" + (6 - len(hex(int(self.hexcolor))[2:])) * '0'\
                   + hex(int(self.hexcolor))[2:]


class BraceletString(models.Model):
    index = models.IntegerField()
    color = models.ForeignKey(BraceletColor, related_name='bracelets')
    bracelet = models.ForeignKey(Bracelet, related_name='strings')

    def __unicode__(self):
        return "[id=" + str(self.id) + ", index=" + str(self.index)\
               + ", color=" + str(self.color) + "]"
    class Meta:
        ordering = ['index']

class BraceletKnotType(models.Model):
    text = models.CharField(max_length=100)

    def __unicode__(self):
        return self.text


class BraceletKnot(models.Model):
    index = models.IntegerField()
    bracelet = models.ForeignKey(Bracelet, related_name='knots')
    knottype = models.ForeignKey(BraceletKnotType, related_name='+')

    def __unicode__(self):
        return "[id=" + str(self.id) + ", index=" + str(self.index)\
            + ", knottype=" + str(self.knottype.id) + ", bracelet="\
            + str(self.bracelet.id) + "]"


class Photo(models.Model):
    name = models.CharField(max_length=50)
    accepted = models.BooleanField(default=False)
    bracelet = models.ForeignKey(Bracelet, related_name='photos')
    user = models.ForeignKey(User, related_name='photos')

    def __unicode__(self):
        return "[id=" + str(self.id) + ", accepted=" + str(self.accepted)\
            + ", bracelet=" + str(self.bracelet.id) + ", user="\
            + self.user.username + "]"


class Rate(models.Model):
    bracelet = models.ForeignKey(Bracelet, related_name='rates')
    rate = models.IntegerField()
    user = models.ForeignKey(User, related_name='rates')
