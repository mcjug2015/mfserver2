''' tests for the api module '''
# pylint: disable=no-member, protected-access
from django.test.testcases import TestCase
from django.contrib.gis.geos.factory import fromstr
from django.contrib.gis.measure import D
from django.db.models import Q
from tastypie.exceptions import NotFound
from django_app.api import ExceptionThrowingModelResource, SaveMeetingResource,\
    MeetingResource
from django_app.models import Meeting
from mockito.mocking import mock


class MeetingTests(TestCase):
    ''' tests for the custom methods of meeting resource '''
    fixtures = ['users_groups_perms.json', 'meetings.json']

    def setUp(self):
        ''' set up the test '''
        self.the_resource = MeetingResource()

    def test_build_filters_empty(self):
        '''
            verify that invoking build filters and passing in nothing returns an
            empty dict
        '''
        self.assertEquals(self.the_resource.build_filters(), {})

    def test_build_filters_existing(self):
        '''
            make sure existing filters that dont have lat, long, and distance in them
            have default tastypie behavior
        '''
        self.assertEquals(self.the_resource.build_filters({'test': 'test'}), {})

    def test_build_filters_location(self):
        '''
            make sure the location filter gets built right when lat, long and distance
            are supplied
        '''
        retval = self.the_resource.build_filters({'lat': 1,
                                                  'long': 1,
                                                  'distance': 1})
        self.assertIn('custom', retval)
        self.assertEquals(retval['custom'].__class__.__name__, 'Q')

    def test_apply_filters_empty(self):
        '''
            Make sure default tastypie behaviour occurs when no custom filter is passed in
        '''
        retval = self.the_resource.apply_filters(None, {})
        self.assertEquals(retval.count(), 2)

    def test_apply_filters_custom(self):
        '''
            Verify that custom location filter applies to queryset when passed in.
        '''
        pnt = fromstr('POINT(%s %s)' % (-77, 39), srid=4326)
        the_dict = {'custom': Q(geo_location__distance_lte=(pnt, D(mi=0.1)))}
        retval = self.the_resource.apply_filters(None, the_dict)
        self.assertEquals(retval.count(), 1)

    def test_apply_sorting_empty(self):
        '''
            Make sure default tastypie behaviour occurs when no custom filter is passed in
        '''
        retval = self.the_resource.apply_sorting(Meeting.objects.all(), {})
        self.assertEquals(retval.count(), 2)
        self.assertEquals(retval[0].name, 'awesome meeting')

    def test_apply_sorting(self):
        '''
            Make sure default tastypie behaviour occurs when no custom filter is passed in
        '''
        retval = self.the_resource.apply_sorting(Meeting.objects.all(),
                                                 {'lat': 39.1, 'long': -77.1, 'distance': 1000,
                                                  'order_by': 'distance'})
        self.assertEquals(retval.count(), 2)
        self.assertEquals(retval[0].name, 'another awesome meeting')


class SaveMeetingTests(TestCase):
    ''' test the custom savemeeting method '''

    def test_save(self):
        ''' test for the custom savemeeting method '''
        bundle = mock()
        bundle.data = {'geo_location': {'coordinates': [-76, 35]}}
        bundle.obj = Meeting()
        retval = SaveMeetingResource().save(bundle)
        self.assertIsNotNone(retval)


class ExceptionThrowingModelResourceTests(TestCase):
    ''' unit tests for the ExceptionThrowingModelResource '''

    def test_real_error(self):
        ''' make sure a real error gets raised '''
        exception = ValueError("testing123")
        self.assertRaises(ValueError, ExceptionThrowingModelResource()._handle_500,
                          None, exception)

    def test_not_found(self):
        ''' make sure a not found exceptions results in a not found response '''
        exception = NotFound()
        response = ExceptionThrowingModelResource()._handle_500(None, exception)
        self.assertTrue(response.status_code, 404)
