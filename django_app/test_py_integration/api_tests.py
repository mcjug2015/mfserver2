''' api integration tests '''
# pylint: disable=no-member
import json
from django.test.testcases import TestCase


class MeetingResourceTests(TestCase):
    ''' integration tests for the MeetingResource '''
    fixtures = ['users_groups_perms.json', 'meetings.json']

    def test_filters(self):
        ''' test filtering '''
        self.client.login(username='test_user', password='testing123')
        filter_str = "/mfserver2/api/v1/meeting/?name__icontains=weso&"
        filter_str += "start_time__gte=20:30:00&"
        filter_str += "day_of_week__in=1&"
        filter_str += "day_of_week__in=3"
        response = self.client.get(filter_str)
        self.assertEquals(response.status_code, 200)
        resp_obj = json.loads(response.content)
        self.assertEquals(resp_obj['meta']['total_count'], 1)
        self.assertEquals(resp_obj['objects'][0]['name'], 'awesome meeting')


class SaveMeetingResourceTest(TestCase):
    ''' integration tests for the SaveMeetingResource '''
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
