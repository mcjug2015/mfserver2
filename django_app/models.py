''' models module '''
# pylint: disable=no-member
from __future__ import unicode_literals
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserConfirmation(models.Model):
    ''' db thing that allows users to confirm accounts '''
    user = models.ForeignKey(User, related_name='confirmations', null=False, blank=False, on_delete=models.CASCADE)
    created_date = models.DateTimeField(null=False, blank=False, default=timezone.now)
    confirmation_key = models.CharField(max_length=64, null=False, blank=False)
    is_confirmed = models.BooleanField(default=False)
    confirmation_date = models.DateTimeField(null=True, blank=True)
    conf_type = models.CharField(max_length=64, null=False, blank=False, default="registration")

    def __unicode__(self):
        return "%s(%s)" % (self.conf_type,
                           self.user.username)

    def __str__(self):
        return self.__unicode__()


class CigarShop(models.Model):
    ''' Model class for a cigar shop, has owner and location '''
    objects = models.Manager()
    name = models.CharField(max_length=250, null=False, blank=False)
    location = models.PointField()
    owner = models.ForeignKey(User, related_name='cigar_shops', null=False, blank=False, on_delete=models.CASCADE)


class MeetingType(models.Model):
    ''' the type of meeting '''
    short_name = models.CharField(null=False, blank=False, max_length=250)
    name = models.CharField(null=False, blank=False, max_length=250)
    description = models.CharField(null=False, blank=False, max_length=250)

    def __unicode__(self):
        return "%s(%s)" % (self.short_name, self.name)

    def __str__(self):
        return self.__unicode__()


class Meeting(models.Model):
    ''' meeting models class '''

    DAY_OF_WEEK_CHOICES = [(1, "Sunday"),
                           (2, "Monday"),
                           (3, "Tuesday"),
                           (4, "Wednesday"),
                           (5, "Thursday"),
                           (6, "Friday"),
                           (7, "Saturday")]

    objects = models.Manager()
    day_of_week = models.IntegerField(null=False, blank=False, choices=DAY_OF_WEEK_CHOICES)
    start_time = models.TimeField(null=False, blank=False)
    end_time = models.TimeField(null=False, blank=False)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=300)
    creator = models.ForeignKey(User, related_name='meetings', null=True, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    geo_location = models.PointField()
    types = models.ManyToManyField(MeetingType, related_name='meetings', blank=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s(%s)" % (self.name, self.creator.username)

    def __str__(self):
        return self.__unicode__()


class MeetingNotThere(models.Model):
    ''' the meeting not there model '''
    meeting = models.ForeignKey(Meeting, related_name='not_theres', null=False, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='not_theres', null=True, blank=True, on_delete=models.SET_NULL)
    note = models.CharField(max_length=200, null=True, blank=True)
    request_host = models.CharField(max_length=200, null=True, blank=True)
    user_agent = models.CharField(max_length=400, null=True, blank=True)
    unique_phone_id = models.CharField(max_length=400, null=True, blank=True)
    resolved = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s, host: %s" % (str(self.pk), str(self.request_host))

    def __str__(self):
        return self.__unicode__()
