''' tests for the converter '''
# pylint: disable=no-member
from django.test.testcases import TestCase
from mockito.mockito import when, unstub
from mockito.matchers import any  # pylint: disable=redefined-builtin
from mockito.mocking import mock
from django_app.old_db_restore import converter
from django_app.models import MeetingType


class GetConnTests(TestCase):
    ''' test the get_conn method '''

    def tearDown(self):
        ''' tear down the test '''
        unstub()

    def test_success(self):
        ''' test getting the mocked connection '''
        when(converter.psycopg2).connect(any()).thenReturn("test123")
        retval = converter.get_conn()
        self.assertEquals(retval, "test123")


class MeetingTypeConverterTests(TestCase):
    ''' test the meetingtype converter '''

    def tearDown(self):
        ''' tear down the test '''
        unstub()

    def test_convert(self):
        ''' make sure list of dicts gets saves as meetingtypes in mfserver2 db '''
        self.assertEquals(MeetingType.objects.all().count(), 0)
        conn = mock()
        cursor = mock()
        when(conn).cursor(cursor_factory=any()).thenReturn(cursor)
        when(cursor).execute(any()).thenReturn(None)
        when(cursor).fetchall().thenReturn([{"id": "1",
                                             "short_name": "a",
                                             "name": "b",
                                             "description": "c"},
                                            {"id": "2",
                                             "short_name": "x",
                                             "name": "y",
                                             "description": "z"}])
        converter.MeetingTypeConverter.convert(conn)
        self.assertEquals(MeetingType.objects.all().count(), 2)
