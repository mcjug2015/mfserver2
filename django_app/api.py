''' module for tastypie endpoints '''
# pylint: disable=too-few-public-methods, no-member
from tastypie import fields
from tastypie.contrib.gis.resources import ModelResource
from django_app.models import MeetingType, Meeting


class MeetingTypeResource(ModelResource):
    ''' get only meeting type endpoint '''

    class Meta(object):
        ''' meta info '''
        queryset = MeetingType.objects.all()
        allowed_methods = ['get']


class MeetingResource(ModelResource):
    ''' meeting endpoint '''
    types = fields.ToManyField(MeetingTypeResource, 'types')

    class Meta(object):
        ''' meta info '''
        queryset = Meeting.objects.all()
        allowed_methods = ['get']
