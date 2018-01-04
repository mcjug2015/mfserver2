''' unit tests for request service '''
# pylint: disable=redefined-builtin,no-self-use
from django.test.testcases import TestCase
from mockito.mockito import when, verify, unstub
from mockito.matchers import any
from mockito.mocking import mock
from django_app.services import request_service


class RequestTests(TestCase):
    ''' tests for the create user method '''

    def tearDown(self):
        ''' tear down test '''
        unstub()

    def setUp(self):
        ''' setup test '''
        self.response = mock()
        when(self.response).raise_for_status().thenReturn(None)

    def test_do_http_method_json(self):
        ''' test the do_http_method with json '''
        when(request_service.requests).post(any(),
                                            verify=False,
                                            headers=any(),
                                            cookies=any(),
                                            json=any()).thenReturn(self.response)
        request_service.do_http_method(request_service.requests.post, "test_url",
                                       "test_referer", "test_token", "test_session_id",
                                       {"test": "test123"})
        verify(self.response).raise_for_status()

    def test_do_http_method_no_json(self):
        ''' test the do_http_method with no json '''
        when(request_service.requests).post(any(),
                                            verify=False,
                                            headers=any(),
                                            cookies=any()).thenReturn(self.response)
        request_service.do_http_method(request_service.requests.post, "test_url",
                                       "test_referer", "test_token", "test_session_id",
                                       None)
        verify(self.response).raise_for_status()

    def test_create_user(self):
        ''' make sure post is invoked '''
        when(self.response).json().thenReturn({"resource_uri": "test_uri"})
        when(request_service).do_http_method(any(), any(), any(),
                                             any(), any(), any()).thenReturn(self.response)
        resource_uri = request_service.create_user({"test": "test123"}, "base_url",
                                                   "referer", "token", "session_id")
        self.assertEqual(resource_uri, "test_uri")
        verify(request_service).do_http_method(any(), any(), any(),
                                               any(), any(), any())

    def test_create_meeting(self):
        ''' make sure post is invoked '''
        when(self.response).json().thenReturn({"resource_uri": "test_meeting_uri"})
        when(request_service).do_http_method(any(), any(), any(),
                                             any(), any(), any()).thenReturn(self.response)
        resource_uri = request_service.create_meeting({"test": "test123"}, "base_url",
                                                      "referer", "token", "session_id")
        self.assertEqual(resource_uri, "test_meeting_uri")
        verify(request_service).do_http_method(any(), any(), any(),
                                               any(), any(), any())

    def test_delete_user(self):
        ''' make sure post is invoked '''
        when(request_service).do_http_method(any(), any(), any(),
                                             any(), any()).thenReturn(None)
        request_service.delete_user("user_uri", "base_url",
                                    "referer", "token", "session_id")
        verify(request_service).do_http_method(any(), any(), any(),
                                               any(), any())
