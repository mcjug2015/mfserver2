''' tests for the admin module '''
# pylint: disable=protected-access, no-member
from django.test.testcases import TestCase
from django_app.admin import MeetingNotThereAdmin
from django_app.models import MeetingNotThere
from django_app import admin
from mockito.mockito import when
from mockito import mock


class LatLongWidgetTests(TestCase):
    ''' Test class for the admin lat long widget '''

    def setUp(self):
        ''' set up the test '''
        self.widget = admin.LatLongWidget()

    def test_decompress_with_value(self):
        ''' test invoking the decompress method with a value '''
        the_value = mock()
        the_value.coords = [1, 2]
        retval = self.widget.decompress(the_value)
        self.assertEqual(retval[0], 2)
        self.assertEqual(retval[1], 1)

    def test_decompress_no_value(self):
        ''' verify that decompressing a falsy value returns a tuple of nones '''
        self.assertEqual(self.widget.decompress([]), (None, None))
        self.assertEqual(self.widget.decompress(None), (None, None))


class LatLongFieldTests(TestCase):
    ''' tests for the admin lat long field '''

    def setUp(self):
        ''' set up the test '''
        self.the_field = admin.LatLongField()

    def test_compress_success(self):
        ''' make sure good data produces a valid point string '''
        retval = self.the_field.compress([1, 2])
        self.assertEqual(retval, 'SRID=4326;POINT(2.000000 1.000000)')

    def test_compress_no_data(self):
        ''' verify that non or empty list returns none '''
        self.assertEqual(self.the_field.compress(None), None)
        self.assertEqual(self.the_field.compress([]), None)

    def test_compress_validation_error(self):
        ''' verify that one of the first two values beeing blanky raises validation '''
        self.assertRaises(admin.forms.ValidationError, self.the_field.compress, [1, {}])
        self.assertRaises(admin.forms.ValidationError, self.the_field.compress, ['', 2])


class CigarShopAdminTests(TestCase):
    ''' tests for the cigar shop admin class '''

    def setUp(self):
        ''' set up the test '''
        mock_model = mock()
        mock_model._meta = None
        self.the_admin = admin.MeetingAdmin(mock_model, None)

    def test_formfield_dbfield_regular(self):
        ''' test default behavior when field name is not 'location' '''
        db_field = mock()
        db_field.name = 'testing'
        retval = self.the_admin.formfield_for_dbfield(db_field, request=mock())
        self.assertNotEquals(type(retval), admin.LatLongField)

    def test_formfield_dbfield_location(self):
        ''' make sure a field named location gets a latlongfield returned '''
        db_field = mock()
        db_field.name = 'geo_location'
        retval = self.the_admin.formfield_for_dbfield(db_field, request=mock())
        self.assertEqual(type(retval), admin.LatLongField)


class MeetingNotThereAdminTests(TestCase):
    ''' tests for the meeting not there admin '''
    fixtures = ['users_groups_perms.json', 'meetings.json']

    def setUp(self):
        ''' set up the test '''
        self.admin = MeetingNotThereAdmin(MeetingNotThere, None)

    def test_deactivate_resolve(self):
        ''' test deactivating and resolving '''
        request = mock()
        when(request).get_full_path().thenReturn("http://www.testing.org")
        queryset = MeetingNotThere.objects.filter(meeting__name='awesome meeting')
        retval = self.admin.deactivate_resolve(request, queryset)
        self.assertEqual(retval['Location'], "http://www.testing.org")
        not_there = MeetingNotThere.objects.get(meeting__name='awesome meeting')
        self.assertTrue(not_there.resolved)
        self.assertFalse(not_there.meeting.is_active)
