''' tests module for auth services '''
from mockito.mockito import when
from mockito.mocking import mock
from mockito.matchers import any  # pylint: disable=redefined-builtin
from django.test.testcases import TestCase
from django_app.services import auth_service


class RefererTokenSessionHelperTests(TestCase):
    ''' tests for RefererTokenSessionHelper class '''

    def test_get_referer(self):
        ''' test the get referer method '''
        helper = auth_service.RefererTokenSessionHelper(None, None, "https://www.test.com/test123/", None)
        self.assertEqual("https://www.test.com", helper.get_referer())

    def test_get_token_session(self):
        ''' test the get token session method '''
        helper = auth_service.RefererTokenSessionHelper("user", "pass", "https://www.test.com/test123/",
                                                        "https://www.test.com/login/")
        when(auth_service.RefererTokenSessionHelper).get_referer().thenReturn("test_referer")
        get_response = mock()
        get_response.text = '<html><body><input value="token1"/></body></html>'
        get_response.cookies = {'csrftoken': 'cookie1'}
        when(auth_service.requests).get("https://www.test.com/test123/", verify=False).thenReturn(get_response)
        post_response = mock()
        post_response.cookies = {'sessionid': 'session_id'}
        when(auth_service.requests).post(any(), headers=any(),
                                         cookies=any(), json=any(),
                                         verify=False).thenReturn(post_response)
        token, session_id = helper.get_token_session()
        self.assertEqual(token, "token1")
        self.assertEqual(session_id, "session_id")
