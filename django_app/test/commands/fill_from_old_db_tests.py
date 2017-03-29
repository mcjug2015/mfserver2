''' tests for the fill_from_old_db command '''
# pylint: disable=no-self-use
from django.test.testcases import TestCase
from mockito.mockito import when, verify
from django_app.management.commands import fill_from_old_db


class FillFromOldDbTests(TestCase):
    ''' tests for the command class '''

    def test_handle(self):
        ''' test the handle method '''
        when(fill_from_old_db.converter).get_conn().thenReturn(None)
        fill_from_old_db.Command().handle()
        verify(fill_from_old_db.converter).get_conn()
