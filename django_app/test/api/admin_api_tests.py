''' unit tests for admin_api '''
from django.test.testcases import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from mockito.mocking import mock
from django_app.api.admin_api import AdminUserResource


class AdminUserResourceTests(TestCase):
    ''' unit tests for the admin resource tests '''

    def test_obj_create(self):
        ''' make sure that obj create saves user and sets password '''
        the_resource = AdminUserResource()
        bundle = mock()
        bundle.request = mock()
        bundle.data = {"username": "deleteme_fake",
                       "is_active": True,
                       "is_staff": False,
                       "last_login": timezone.now(),
                       "email": "fake_email@test.com",
                       "date_joined": timezone.now(),
                       "password": "The_fakeP@ssword"}
        the_resource.obj_create(bundle)
        the_user = User.objects.get(username="deleteme_fake")
        self.assertTrue(the_user.check_password("The_fakeP@ssword"))
