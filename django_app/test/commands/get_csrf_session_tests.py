''' module for get_csrf_session command tests '''
# pylint: disable=redefined-builtin
from django.test.testcases import TestCase
from django_app.management.commands import get_csrf_session
from mockito.mocking import mock
from mockito.mockito import when, verify, unstub
from mockito.matchers import any


class CommandTests(TestCase):
    ''' class for the command tests '''

    def setUp(self):
        ''' set up the test '''
        self.command = get_csrf_session.Command()

    def tearDown(self):
        ''' tear down test '''
        unstub()

    def test_handle(self):
        ''' verify the handle method invokes the expected methods '''
        when(get_csrf_session.RefererTokenSessionHelper).get_referer().thenReturn("test1")
        when(get_csrf_session.RefererTokenSessionHelper).get_token_session().thenReturn(("test2", "test3"))
        retval = self.command.handle(username='a',
                                     password='b',
                                     initial_url='https://example.com:8000',
                                     login_url='d')
        expected = 'curl -f -k -v --cookie "csrftoken=test2;sessionid=test3"'
        expected += ' -H "X-CSRFToken: test2" -H "referer: test1"'
        self.assertEqual(expected, retval)

    def test_add_arguments(self):
        ''' make sure add arguments method adds 4 arguments '''
        the_parser = mock()
        when(the_parser).add_argument(any(), default=any()).thenReturn(None)
        self.command.add_arguments(the_parser)
        verify(the_parser, times=4).add_argument(any(), default=any())
