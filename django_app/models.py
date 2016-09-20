from __future__ import unicode_literals
from django.contrib.gis.db import models
from django.contrib.auth.models import User


class CigarShop(models.Model):
    ''' Model class for a cigar shop, has owner and location '''
    objects = models.GeoManager()
    name = models.CharField(max_length=250, null=False, blank=False)
    location = models.PointField()
    owner = models.ForeignKey(User, related_name='cigar_shops', null=False, blank=False)

    def __str__(self):
        return self.name
