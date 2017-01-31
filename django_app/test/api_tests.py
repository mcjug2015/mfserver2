''' tests for the api module '''
# pylint: disable=no-member, protected-access
import json
from django.test.testcases import TestCase
from tastypie.exceptions import NotFound
from django_app.api import ExceptionThrowingModelResource


class ExceptionThrowingModelResourceTests(TestCase):
    ''' unit tests for the ExceptionThrowingModelResource '''

    def test_real_error(self):
        ''' make sure a real error gets raised '''
        exception = ValueError("testing123")
        self.assertRaises(ValueError, ExceptionThrowingModelResource()._handle_500,
                          None, exception)

    def test_not_found(self):
        ''' make sure a not found exceptions results in a not found response '''
        exception = NotFound()
        response = ExceptionThrowingModelResource()._handle_500(None, exception)
        self.assertTrue(response.status_code, 404)


class SaveMeetingResourceTest(TestCase):
    ''' unit tests for the SaveMeetingResource '''
    fixtures = ['users_groups_perms.json', 'meetings.json']

    def test_post(self):
        ''' make sure posting a meeting works '''
        self.client.login(username='test_user', password='testing123')
        response = self.client.get('/mfserver2/api/v1/savemeeting/')
        self.assertEquals(response.status_code, 200)
        resp_obj = json.loads(response.content)
        self.assertEquals(resp_obj['meta']['total_count'], 2)
        meeting_obj = {"geo_location": {"coordinates": [-77.0, 39.0], "type": "Point"},
                       "name": "posted meeting",
                       "creator": "/mfserver2/api/v1/auth/user/1/",
                       "day_of_week": 7,
                       "start_time": "22:30+03:00",
                       "end_time": "23:30+03:00",
                       "description": "posted meeting",
                       "address": "another address",
                       "is_active": True,
                       "types": []}
        response = self.client.post('/mfserver2/api/v1/savemeeting/',
                                    json.dumps(meeting_obj),
                                    content_type='application/json')
        self.assertEquals(response.status_code, 201)
        response = self.client.get('/mfserver2/api/v1/savemeeting/')
        self.assertEquals(response.status_code, 200)
        resp_obj = json.loads(response.content)
        self.assertEquals(resp_obj['meta']['total_count'], 3)
