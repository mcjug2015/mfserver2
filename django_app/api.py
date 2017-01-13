''' module for tastypie endpoints '''
# pylint: disable=too-few-public-methods, no-member
from tastypie import fields
from tastypie.contrib.gis.resources import ModelResource
from tastypie.constants import ALL
from django.contrib.auth.models import User
from django_app.models import MeetingType, Meeting
from django_app.auth import UserObjectsAuthorization


class UserResource(ModelResource):
    ''' Use this to get info about the currently logged in user. '''

    class Meta(object):
        ''' meta info '''
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        queryset = User.objects.all()
        resource_name = 'auth/user'
        excludes = ['password', 'is_superuser']
        authorization = UserObjectsAuthorization()
        filtering = {'username': ALL}


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
