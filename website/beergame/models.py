from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from django_extensions.db.models import TimeStampedModel

class Game(TimeStampedModel):
    name = models.CharField(_('name'), max_length=30)
    total_periods = models.IntegerField(_('total number of periods'),
        default=50)
    is_public = models.BooleanField(_('is public?'), default=False)

    def __unicode__(self):
        return self.name

class Team(TimeStampedModel):
    name = models.CharField(_('name'), max_length=30)

    def __unicode__(self):
        return self.name

class TeamMember(TimeStampedModel):
    ROLE_CHOICES = (
        ('Factory','Factory'),
        ('Distributor','Distributor'),
        ('Wholesaler','Wholesaler'),
        ('Retailer','Retailer')
        )
    user = models.ForeignKey(User)
    role = models.CharField(_('role in supply chain'), max_length=20,
        choices=ROLE_CHOICES)
    team = models.ForeignKey(Team)

    def __unicode__(self):
        return self.user.username

class Period(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(TeamMember)
    number = models.IntegerField(_('period number'), default=0)
    inventory = models.IntegerField(_('number of items in inventory'),
        default=100)
    backorder = models.IntegerField(_('number of back-orders'), default=0)
    demand = models.IntegerField(_('demand of this period'), default=100)
    order = models.IntegerField(_('number of items to be ordered'),
        default=100)
    shipment = models.IntegerField(_('shipment to be recieved in this week'),
        default=100)
    cost = models.FloatField(_('cost of this period'), default=0.0)

    def __unicode__(self):
        return 'period number \"%d\" for \"%s\" in game \"%s\"'%(self.number,
            self.player.user.username, self.game.name)

    def calculate_cost(self):
        return self.inventory*0.5 + self.backorder


