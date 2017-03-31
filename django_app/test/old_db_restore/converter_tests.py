''' tests for the converter '''
# pylint: disable=no-member, no-self-use
from django.test.testcases import TestCase
from django.contrib.auth.models import User
from mockito.mockito import when, unstub, verify
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


class ConverterDriverTests(TestCase):
    ''' tests for the converter driver '''

    def tearDown(self):
        ''' tear down the test '''
        unstub()

    def test_run(self):
        '''run method invokes expected things '''
        conn = mock()
        cursor = mock()
        test_converter = mock()
        when(converter).get_conn().thenReturn(conn)
        when(conn).cursor(cursor_factory=any()).thenReturn(cursor)
        when(cursor).execute(any()).thenReturn(None)
        when(cursor).fetchall().thenReturn(["testing123"])
        when(test_converter).get_sql().thenReturn(None)
        when(test_converter).convert_one(any()).thenReturn(None)
        converter.ConverterDriver([test_converter]).run()
        verify(test_converter).convert_one(any())


class MeetingTypeConverterTests(TestCase):
    ''' test the meetingtype converter '''

    def test_get_sql(self):
        ''' make sure the right sql is returned '''
        self.assertEquals("select id, short_name, name, description from aabuddy_meetingtype",
                          converter.MeetingTypeConverter.get_sql())

    def test_convert_one(self):
        ''' make sure convert one creates expected meeting type entry in mfserver2 db '''
        old_item = {"id": "1",
                    "short_name": "a",
                    "name": "b",
                    "description": "c"}
        self.assertEquals(MeetingType.objects.all().count(), 0)
        converter.MeetingTypeConverter.convert_one(old_item)
        self.assertEquals(MeetingType.objects.all().count(), 1)


class UserConverterTests(TestCase):
    ''' test the meetingtype converter '''

    def test_get_sql(self):
        ''' make sure the right sql is returned '''
        self.assertIn("from auth_user",
                      converter.UserConverter.get_sql())

    def test_convert_one(self):
        ''' make sure convert one creates expected meeting type entry in mfserver2 db '''
        old_item = {"id": "500000",
                    "password": "pbkdf2_sha256$10000$dDGKHQSXUXfs$auU8lSE+YT7CkZ/4SMdPLRrBCdU90mx242r9MrX024U=",
                    "last_login": "2014-01-15 20:26:41.011102-05",
                    "is_superuser": False,
                    "username": "mooo@test.com",
                    "first_name": "NOT SET",
                    "last_name": "NOT SET",
                    "email": "mooo@test.com",
                    "is_staff": False,
                    "is_active": False,
                    "date_joined": "2014-01-11 14:43:15.812485-05"}
        self.assertEquals(User.objects.all().count(), 1)
        converter.UserConverter.convert_one(old_item)
        self.assertEquals(User.objects.all().count(), 2)
