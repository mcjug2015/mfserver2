''' module for tastypie endpoints '''
# pylint: disable=too-few-public-methods, no-member, misplaced-bare-raise
import logging
from tastypie import fields
from tastypie.contrib.gis.resources import ModelResource
from tastypie.constants import ALL
from tastypie.authentication import SessionAuthentication
from tastypie.exceptions import NotFound
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404, HttpResponseNotFound
from django.contrib.auth.models import User
from django_app.models import MeetingType, Meeting
from django_app.auth import UserObjectsAuthorization,\
    OwnerObjectsOnlyAuthorization
LOGGER = logging.getLogger(__name__)


class ExceptionThrowingModelResource(ModelResource):
    ''' resource that does not eat exceptions '''

    def _handle_500(self, request, exception):
        ''' stop swollowing legitimate exceptions '''
        not_found_exceptions = (NotFound, ObjectDoesNotExist, Http404)
        if isinstance(exception, not_found_exceptions):
            return HttpResponseNotFound()
        else:
            LOGGER.error('Something went wrong in tastypie, details below')
            LOGGER.exception(exception)
            raise exception


class UserResource(ExceptionThrowingModelResource):
    ''' Use this to get info about the currently logged in user. '''

    class Meta(object):
        ''' meta info '''
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        queryset = User.objects.all()
        resource_name = 'auth/user'
        excludes = ['password', 'is_superuser']
        authentication = SessionAuthentication()
        authorization = UserObjectsAuthorization()
        filtering = {'username': ALL}


class MeetingTypeResource(ExceptionThrowingModelResource):
    ''' get only meeting type endpoint '''

    class Meta(object):
        ''' meta info '''
        queryset = MeetingType.objects.all()
        allowed_methods = ['get']


class MeetingResource(ExceptionThrowingModelResource):
    ''' meeting endpoint '''
    creator = fields.ToOneField(UserResource, 'creator')
    types = fields.ToManyField(MeetingTypeResource, 'types')

    class Meta(object):
        ''' meta info '''
        queryset = Meeting.objects.all()
        allowed_methods = ['get']


class SaveMeetingResource(ExceptionThrowingModelResource):
    ''' meeting endpoint for saving meetings '''
    creator = fields.ToOneField(UserResource, 'creator')
    types = fields.ToManyField(MeetingTypeResource, 'types')

    class Meta(object):
        ''' meta info '''
        queryset = Meeting.objects.all()
        allowed_methods = ['get', 'post']
        authentication = SessionAuthentication()
        authorization = OwnerObjectsOnlyAuthorization()
