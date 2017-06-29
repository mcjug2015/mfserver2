''' not sure if it makes sense to test a fabfile, but i guess it doesn't hurt '''
# pylint: disable=no-self-use
from django.test.testcases import TestCase
from mockito.mockito import when, verify, unstub
from mockito.matchers import any  # pylint: disable=redefined-builtin
from django_app.old_db_restore import fab_restore


class RestoreTests(TestCase):
    ''' tests for the restore fab function '''

    def tearDown(self):
        ''' tear down the test '''
        unstub()

    def test_success(self):
        ''' make sure restore invokes the local method 4 times '''
        when(fab_restore).local(any()).thenReturn(None)
        fab_restore.restore("testing", "testing")
        verify(fab_restore, times=7).local(any())


class SudoOldToNewTests(TestCase):
    ''' tests for the old to new fab function '''

    def tearDown(self):
        ''' tear down the test '''
        unstub()

    def test_success(self):
        ''' make sure restore invokes the local method 4 times '''
        when(fab_restore).local(any()).thenReturn(None)
        fab_restore.sudo_reload_db()
        verify(fab_restore, times=3).local(any())
