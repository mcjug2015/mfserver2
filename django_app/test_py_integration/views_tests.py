''' test module for views integration tests '''
# pylint: disable=no-member, no-self-use
import json
from django.test.testcases import TestCase
from django.contrib.auth.models import User
from mockito.mockito import unstub, when, verify
from mockito.matchers import any  # pylint: disable=redefined-builtin
from django_app.models import UserConfirmation
from django_app import views


class TestUserCreation(TestCase):
    ''' roundtrip integration test for user registration '''

    def setUp(self):
        ''' set up the test '''
        when(views.django_mail).send_mail(subject=any(), message=any(),
                                          from_email=any(),
                                          recipient_list=any(),
                                          fail_silently=any()).thenReturn(None)

    def tearDown(self):
        ''' tear down test '''
        unstub()

    def test_registration_roundtrip(self):
        ''' make sure we can register a user and submit/get meetings with him '''
        self.assertEquals(UserConfirmation.objects.all().count(), 0)
        response = self.client.post("/mfserver2/register/",
                                    content_type='application/json',
                                    data=json.dumps({"email": "test1234@test.com",
                                                     "password": "fake123"}))
        self.assertEquals(response.status_code, 201)
        verify(views.django_mail).send_mail(subject=any(), message=any(),
                                            from_email=any(),
                                            recipient_list=any(),
                                            fail_silently=any())
        conf = UserConfirmation.objects.get(user__email='test1234@test.com')
        response = self.client.get("/mfserver2/register/", {"confirmation": conf.confirmation_key})
        self.assertEquals(response.status_code, 200)
        self.client.login(username='test1234@test.com', password='fake123')
        response = self.client.get('/mfserver2/api/v1/savemeeting/')
        self.assertEquals(response.status_code, 200)
        resp_obj = json.loads(response.content)
        self.assertEquals(resp_obj['meta']['total_count'], 0)
        user_pk = User.objects.get(email='test1234@test.com').pk
        meeting_obj = {"geo_location": {"coordinates": ['-77.0', '39.0'], "type": "Point"},
                       "name": "roundtrip meeting",
                       "creator": "/mfserver2/api/v1/auth/user/%s/" % user_pk,
                       "day_of_week": 7,
                       "start_time": "21:30",
                       "end_time": "22:30",
                       "description": "roundtrip meeting",
                       "address": "roundtrip address",
                       "types": [],
                       "is_active": True}
        response = self.client.post('/mfserver2/api/v1/savemeeting/',
                                    json.dumps(meeting_obj),
                                    content_type='application/json')
        self.assertEquals(response.status_code, 201)
        response = self.client.get('/mfserver2/api/v1/savemeeting/')
        self.assertEquals(response.status_code, 200)
        resp_obj = json.loads(response.content)
        self.assertEquals(resp_obj['meta']['total_count'], 1)
