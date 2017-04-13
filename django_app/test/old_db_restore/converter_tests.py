''' tests for the converter '''
# pylint: disable=no-member, no-self-use
from django.test.testcases import TestCase
from mockito.mockito import when, unstub, verify
from mockito.matchers import any  # pylint: disable=redefined-builtin
from mockito.mocking import mock
from django_app.old_db_restore import converter


class GetConnTests(TestCase):
    ''' test the get_conn method '''

    def tearDown(self):
        ''' tear down the test '''
        unstub()

    def test_success(self):
        ''' test getting the mocked connection '''
        connection = mock()
        when(converter.psycopg2).connect(any()).thenReturn(connection)
        when(connection).set_client_encoding(any()).thenReturn(None)
        converter.get_conn()
        verify(connection).set_client_encoding(any())


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
        manager = mock()
        result_set = mock()
        when(converter).get_conn().thenReturn(conn)
        when(conn).cursor(cursor_factory=any()).thenReturn(cursor)
        when(cursor).execute(any()).thenReturn(None)
        when(cursor).fetchall().thenReturn(["testing123"])
        when(test_converter).get_sql().thenReturn(None)
        when(test_converter).collect_id(any()).thenReturn(None)
        when(test_converter).collect_item(any()).thenReturn(None)
        when(test_converter).get_manager().thenReturn(manager)
        when(manager).filter(pk__in=any()).thenReturn(result_set)
        when(manager).bulk_create(any(), batch_size=any()).thenReturn(None)
        when(result_set).delete().thenReturn(None)
        converter.ConverterDriver([test_converter]).run()
        verify(test_converter).collect_item(any())
        verify(manager).bulk_create(any(), batch_size=any())


class MeetingTypeConverterTests(TestCase):
    ''' test the meetingtype converter '''

    def setUp(self):
        ''' set up the test '''
        self.converter = converter.MeetingTypeConverter()

    def test_get_sql(self):
        ''' make sure the right sql is returned '''
        self.assertEquals("select id, short_name, name, description from aabuddy_meetingtype",
                          converter.MeetingTypeConverter.get_sql())

    def test_collect_id(self):
        ''' collect id saves the id '''
        old_item = {"id": "1"}
        self.assertEquals(len(self.converter.ids), 0)
        self.converter.collect_id(old_item)
        self.assertEquals(len(self.converter.ids), 1)

    def test_collect_item(self):
        ''' make sure convert one creates expected meeting type entry in mfserver2 db '''
        old_item = {"id": "1",
                    "short_name": "a",
                    "name": "b",
                    "description": "c"}
        self.assertEquals(len(self.converter.new_objs), 0)
        self.converter.collect_item(old_item)
        self.assertEquals(len(self.converter.new_objs), 1)

    def test_get_manager(self):
        ''' manage is meetingtype manager '''
        self.assertEquals(self.converter.get_manager().model.__name__, 'MeetingType')


class UserConverterTests(TestCase):
    ''' test the user converter '''

    def setUp(self):
        ''' set up the test '''
        self.converter = converter.UserConverter()

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
        self.assertEquals(len(self.converter.new_objs), 0)
        self.converter.collect_item(old_item)
        self.assertEquals(len(self.converter.new_objs), 1)

    def test_get_manager(self):
        ''' manage is meetingtype manager '''
        self.assertEquals(self.converter.get_manager().model.__name__, 'User')


class MeetingConverterTests(TestCase):
    ''' test the meeting converter '''

    def setUp(self):
        ''' set up the test '''
        self.converter = converter.MeetingConverter()

    def test_get_sql(self):
        ''' make sure the right sql is returned '''
        self.assertIn("from aabuddy_meeting",
                      converter.MeetingConverter.get_sql())

    def test_get_manager(self):
        ''' manage is meetingtype manager '''
        self.assertEquals(self.converter.get_manager().model.__name__, 'Meeting')

    def test_convert_one(self):
        ''' make sure convert one creates expected meeting type entry in mfserver2 db '''
        old_item = {"id": "500000",
                    "day_of_week": "1",
                    "start_time": "19:00:00",
                    "end_time": "20:00:00",
                    "name": "mooo",
                    "description": "mooo",
                    "creator_id": "1",
                    "address": "mooo",
                    "created_date": "2013-12-21 12:40:38.334359-05",
                    "st_astext": "POINT(-121.2717698 38.1397487)"}
        self.assertEquals(len(self.converter.new_objs), 0)
        self.converter.collect_item(old_item)
        self.assertEquals(len(self.converter.new_objs), 1)


class MeetingToTypeConverterTests(TestCase):
    ''' test the meeting to type converter '''

    def setUp(self):
        ''' set up the test '''
        self.converter = converter.MeetingToTypeConverter()

    def test_get_sql(self):
        ''' make sure the right sql is returned '''
        self.assertIn("from aabuddy_meeting_types",
                      converter.MeetingToTypeConverter.get_sql())

    def test_get_manager(self):
        ''' manage is meetingtype manager '''
        self.assertEquals(self.converter.get_manager().model.__name__, 'Meeting_types')

    def test_convert_one(self):
        ''' make sure convert one creates expected meeting type entry in mfserver2 db '''
        old_item = {"id": "500000",
                    "meeting_id": "1",
                    "meetingtype_id": "1"}
        self.assertEquals(len(self.converter.new_objs), 0)
        self.converter.collect_item(old_item)
        self.assertEquals(len(self.converter.new_objs), 1)
