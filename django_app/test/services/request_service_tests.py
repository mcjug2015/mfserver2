''' unit tests for request service '''
# pylint: disable=redefined-builtin,no-self-use
from django.test.testcases import TestCase
from django_app.services import request_service
from mockito.mockito import when, verify, unstub
from mockito.matchers import any
from mockito.mocking import mock


class CreateUserTests(TestCase):
    ''' tests for the create user method '''

    def tearDown(self):
        ''' tear down test '''
        unstub()

    def test_create_user(self):
        ''' make sure post is invoked '''
        response = mock()
        when(response).raise_for_status().thenReturn(None)
        when(request_service.requests).post(any(),
                                            json=any(),
                                            headers=any(),
                                            cookies=any(),
                                            verify=False).thenReturn(response)
        request_service.create_user({}, "base_url", "referer", "token", "session_id")
        verify(response).raise_for_status()
