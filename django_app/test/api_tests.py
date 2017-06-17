''' tests for the api module '''
# pylint: disable=no-member, redefined-builtin, protected-access
from django.test.testcases import TestCase
from django.contrib.gis.geos.factory import fromstr
from django.contrib.gis.measure import D
from django.db.models import Q
from django.contrib.auth.models import User
from django.http.request import QueryDict
from tastypie.exceptions import NotFound
from django_app.api import ExceptionThrowingModelResource, SaveMeetingResource,\
    MeetingResource, MeetingValidation, MeetingNotThereResource, ModelResource
from django_app.models import Meeting, MeetingNotThere
from mockito.mocking import mock
from mockito.mockito import when, unstub
from mockito.matchers import any


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

    def test_full_hydrate(self):
        ''' full hydrate sets creator to request user '''
        bundle = mock()
        bundle.request = mock()
        bundle.request.user = User(username="test123")
        bundle.obj = Meeting()
        when(ModelResource).full_hydrate(any()).thenReturn(bundle)
        SaveMeetingResource().full_hydrate(bundle)
        self.assertEquals(bundle.obj.creator.username, "test123")


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


class MeetingValidationTests(TestCase):
    ''' tests for the meeting validation class '''

    def setUp(self):
        ''' set up test '''
        self.meeting_validation = MeetingValidation()
        self.meeting_obj = {"geo_location": {"coordinates": ['-77.0', '39.0'],
                                             "type": "Point"},
                            "name": "test meeting",
                            "creator": "irrelevant here",
                            "day_of_week": 7,
                            "start_time": "22:30",
                            "end_time": "23:30",
                            "description": "test meeting",
                            "address": "test address",
                            "is_active": True,
                            "types": []}
        self.bundle = mock()
        self.bundle.data = self.meeting_obj

    def test_fail_on_form(self):
        ''' fail when one of the form defined validations fails '''
        self.meeting_obj['day_of_week'] = 85
        retval = self.meeting_validation.is_valid(self.bundle)
        self.assertIsNotNone(retval)
        self.assertIn('day_of_week', retval)

    def test_fail_on_lat(self):
        ''' fail with an invalid latitude '''
        self.meeting_obj['geo_location']['coordinates'][1] = 91
        retval = self.meeting_validation.is_valid(self.bundle)
        self.assertIn('geo_location', retval)

    def test_fail_on_long(self):
        ''' fail with an invalid longitude '''
        self.meeting_obj['geo_location']['coordinates'][0] = -180.01
        retval = self.meeting_validation.is_valid(self.bundle)
        self.assertIn('geo_location', retval)

    def test_pass_validation(self):
        ''' pass validation '''
        self.assertFalse(self.meeting_validation.is_valid(self.bundle))


class MeetingNotThereResourceTests(TestCase):
    ''' test the meeting not there resource '''

    def setUp(self):
        ''' set up the test '''
        self.bundle = mock()
        self.bundle.obj = MeetingNotThere()
        self.bundle.request = mock()
        self.bundle.request.META = QueryDict(mutable=True)
        self.bundle.request.META.update({"REMOTE_ADDR": "a",
                                         "HTTP_USER_AGENT": "b"})
        when(ModelResource).full_hydrate(any()).thenReturn(self.bundle)
        self.resource = MeetingNotThereResource()

    def tearDown(self):
        ''' tear down test '''
        unstub()

    def test_full_hydrate(self):
        ''' writes the special fields to object '''
        self.bundle.request.user = User.objects.get(username="mf_admin")
        retval = self.resource.full_hydrate(self.bundle)
        self.assertEquals(retval.obj.user.username, "mf_admin")

    def test_full_hydrate_no_user(self):
        ''' writes special fields with no logged in user '''
        self.bundle.request.user = mock()
        when(self.bundle.request.user).is_authenticated().thenReturn(False)
        retval = self.resource.full_hydrate(self.bundle)
        self.assertIsNone(retval.obj.user)
        self.assertEquals(retval.obj.request_host, "a")
        self.assertEquals(retval.obj.user_agent, "b")
