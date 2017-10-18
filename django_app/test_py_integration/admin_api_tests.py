''' integration tests for admin api endpoints '''
import json
from django.test.testcases import TestCase
from django.utils import timezone
from django.contrib.auth.models import User


class AdminUserResourceTests(TestCase):
    ''' integration tests for admin user resource '''

    def test_create_delete(self):
        ''' create delete users '''
        self.client.login(username='mf_admin', password='mf_admin')
        user_obj = {"username": "deleteme_fake",
                    "is_active": True,
                    "is_staff": False,
                    "last_login": str(timezone.now()),
                    "email": "fake_email@test.com",
                    "date_joined": str(timezone.now()),
                    "password": "The_fakeP@ssword"}
        response = self.client.post('/mfserver2/admin_api/v1/admin_user/',
                                    json.dumps(user_obj),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.filter(username='deleteme_fake').count(), 1)
        self.client.login(username='deleteme_fake', password='The_fakeP@ssword')
        response = self.client.get("/mfserver2/api/v1/auth/user/")
        self.assertEqual(response.status_code, 200)
        user_obj = json.loads(response.content.decode('utf8'))
        user_obj = user_obj['objects'][0]
        self.assertEqual(user_obj["username"], "deleteme_fake")
        self.client.login(username='mf_admin', password='mf_admin')
        self.client.delete('/mfserver2/admin_api/v1/admin_user/%s/' % user_obj["id"])
        self.assertEqual(User.objects.filter(username='deleteme_fake').count(), 0)
