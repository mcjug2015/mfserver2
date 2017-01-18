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
        response1 = mock()
        response1.text = '<html><body><input value="token1"/></body></html>'
        response1.cookies = {'csrftoken': 'cookie1'}
        when(get_csrf_session.requests).get(any(), verify=False).thenReturn(response1)
        response2 = mock()
        response2.cookies = {'csrftoken': 'cookie2',
                             'sessionid': 'session_cookie1'}
        when(get_csrf_session.requests).post(any(), headers=any(),
                                             cookies=any(), json=any(),
                                             verify=False).thenReturn(response2)
        retval = self.command.handle(username='a',
                                     password='b',
                                     initial_url='https://example.com:8000',
                                     login_url='d')
        self.assertEquals('curl -f -k -v --cookie "csrftoken=cookie2" --cookie "sessionid=session_cookie1"',
                          retval)

    def test_add_arguments(self):
        ''' make sure add arguments method adds 4 arguments '''
        the_parser = mock()
        when(the_parser).add_argument(any(), default=any()).thenReturn(None)
        self.command.add_arguments(the_parser)
        verify(the_parser, times=4).add_argument(any(), default=any())
