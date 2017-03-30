''' tests for the converter '''
from django.test.testcases import TestCase
from mockito.mockito import when, unstub
from mockito.matchers import any  # pylint: disable=redefined-builtin
from django_app.old_db_restore import converter


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
