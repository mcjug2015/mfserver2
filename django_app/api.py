''' module for tastypie endpoints '''
# pylint: disable=too-few-public-methods, no-member, misplaced-bare-raise, too-many-boolean-expressions
import logging
from tastypie import fields
from tastypie.contrib.gis.resources import ModelResource
from tastypie.constants import ALL
from tastypie.authentication import SessionAuthentication
from tastypie.exceptions import NotFound
from tastypie.validation import FormValidation, Validation
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404, HttpResponseNotFound
from django.contrib.gis.measure import D
from django.contrib.gis.geos.geometry import GEOSGeometry
from django.contrib.auth.models import User
from django.contrib.gis.geos.factory import fromstr
from django_app.models import MeetingType, Meeting
from django_app.auth import UserObjectsAuthorization,\
    OwnerObjectsOnlyAuthorization
from django_app.forms import MeetingForm
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
        max_limit = 50


class MeetingResource(ExceptionThrowingModelResource):
    ''' meeting endpoint '''
    creator = fields.ToOneField(UserResource, 'creator')
    types = fields.ToManyField(MeetingTypeResource, 'types')

    def build_filters(self, filters=None, ignore_bad_filters=False):
        if filters is None:
            filters = {}
        orm_filters = super(MeetingResource, self).build_filters(filters)
        if 'lat' in filters and 'long' in filters and 'distance' in filters:
            pnt = fromstr('POINT(%s %s)' % (filters['long'], filters['lat']), srid=4326)
            orm_filters.update({'custom': Q(geo_location__distance_lte=(pnt, D(mi=filters['distance'])))})
        return orm_filters

    def apply_filters(self, request, applicable_filters):
        if 'custom' in applicable_filters:
            custom = applicable_filters.pop('custom')
        else:
            custom = None
        semi_filtered = super(MeetingResource, self).apply_filters(request, applicable_filters)
        return semi_filtered.filter(custom) if custom else semi_filtered

    def apply_sorting(self, objects, options=None):
        if options and 'lat' in options and 'long' in options and 'distance' in options and\
                'order_by' in options and options['order_by'] == 'distance':
            pnt = fromstr('POINT(%s %s)' % (options['long'], options['lat']), srid=4326)
            return objects.distance(pnt).order_by('distance')
        return super(MeetingResource, self).apply_sorting(objects, options)

    class Meta(object):
        ''' meta info '''
        queryset = Meeting.objects.all()
        allowed_methods = ['get']
        filtering = {'name': ('icontains'),
                     'start_time': ('gte'),
                     'day_of_week': (ALL)}
        ordering = ['name', 'start_time', 'day_of_week']
        max_limit = 50


class MeetingValidation(Validation):
    ''' custom validation that does extra stuff meeting validation can not do '''

    def __init__(self):
        super(MeetingValidation, self).__init__()
        self.form_validation = FormValidation(form_class=MeetingForm)

    def is_valid(self, bundle, request=None):
        errors = self.form_validation.is_valid(bundle, request)
        if errors:
            return errors
        coordinates = bundle.data['geo_location']['coordinates']
        coordinates = [float(coordinates[0]), float(coordinates[1])]
        if coordinates[0] < -180 or coordinates[0] > 180:
            errors['geo_location'] = "Longitude must be between -180 and 180, it is %s" % coordinates[0]
        if coordinates[1] < -90 or coordinates[1] > 90:
            errors['geo_location'] = "Lattitude must be between -90 and 90, it is %s" % coordinates[1]
        return errors


class SaveMeetingResource(ExceptionThrowingModelResource):
    ''' meeting endpoint for saving meetings '''
    creator = fields.ToOneField(UserResource, 'creator')
    types = fields.ToManyField(MeetingTypeResource, 'types')

    def save(self, bundle, skip_errors=False):
        '''
            custom save method.
            if this is not done saving causes
            GDALException: Invalid geometry pointer returned from "OGR_G_CreateGeometryFromJson".
            when run in nginx/uwsgi, but not in runserver. no idea why.
            -1.5 weeks of life to figure this out.
        '''
        point_str = 'POINT(%s %s)' % (bundle.data['geo_location']['coordinates'][0],
                                      bundle.data['geo_location']['coordinates'][1])
        bundle.obj.geo_location = GEOSGeometry(point_str, srid=4326)
        LOGGER.debug("geolocation instance is %s", bundle.obj.geo_location.__class__.__name__)
        LOGGER.debug("geolocation is %s", bundle.obj.geo_location)
        return super(SaveMeetingResource, self).save(bundle, skip_errors)

    class Meta(object):
        ''' meta info '''
        queryset = Meeting.objects.all()
        allowed_methods = ['get', 'post']
        authentication = SessionAuthentication()
        authorization = OwnerObjectsOnlyAuthorization()
        validation = MeetingValidation()
        max_limit = 50
