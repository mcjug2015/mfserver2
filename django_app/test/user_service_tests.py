''' tests module for user_service '''
# pylint: disable=no-member
import datetime
from django.utils import timezone
from django.test.testcases import TestCase
from django.contrib.auth.models import User
from mockito.mockito import when, unstub
from mockito.matchers import any  # pylint: disable=redefined-builtin
from django_app.models import UserConfirmation
from django_app.services import user_service


class GetUserToRegisterTests(TestCase):
    ''' tests for the get user to register method '''

    def test_existing_user_fail(self):
        ''' make sure existing user with and without confs is not elligible to register '''
        result = user_service.get_user_to_register("test@test.com", "admin")
        self.assertIsNone(result["user"])

        user = User.objects.get(username="admin")
        user_confirmation = UserConfirmation(user=user)
        user_confirmation.expiration_date = timezone.now() + datetime.timedelta(days=3)
        user_confirmation.save()
        result = user_service.get_user_to_register("test@test.com", "admin")
        self.assertIsNone(result["user"])

    def test_existing_user_success(self):
        ''' make sure existing user with unconfirmed, expired conf can register '''
        user = User.objects.get(username="admin")
        user.is_active = False
        user.save()
        user_confirmation = UserConfirmation(user=user)
        user_confirmation.expiration_date = timezone.now() - datetime.timedelta(days=50)
        user_confirmation.save()
        result = user_service.get_user_to_register("test@test.com", "admin")
        self.assertIn("inactive user", result["status"])
        self.assertEquals(result["user"].email, "test@test.com")

    def test_new_user(self):
        ''' test getting a new user back '''
        result = user_service.get_user_to_register("test@mooo.com", "testusername")
        self.assertEquals(result["status"], "brand new user testusername")
        self.assertEquals(result["user"].email, "test@mooo.com")


class CreateUserAnConfTests(TestCase):
    ''' test class for the create_user_and_conf method '''

    def tearDown(self):
        ''' tear down test '''
        unstub()

    def test_no_user(self):
        ''' make sure nothing happens if user should not be registered '''
        self.assertEquals(User.objects.all().count(), 1)
        self.assertEquals(UserConfirmation.objects.all().count(), 0)
        when(user_service).get_user_to_register(any(), any()).thenReturn({"status": "no",
                                                                          "user": None})
        result = user_service.create_user_and_conf('test1234@test.com', 'mooo1', 'mooo1')
        self.assertEquals(User.objects.all().count(), 1)
        self.assertEquals(UserConfirmation.objects.all().count(), 0)
        self.assertEquals(result["status"], "no")

    def test_success(self):
        ''' make sure method successfully creates user and conf '''
        self.assertEquals(User.objects.all().count(), 1)
        self.assertEquals(UserConfirmation.objects.all().count(), 0)
        user = User(pk=1000, username='mooo1', email='test1234@test.com', first_name='NOT_SET', last_name='NOT_SET',
                    is_active=False, is_superuser=False, is_staff=False)
        when(user_service).get_user_to_register(any(), any()).thenReturn({"user": user})
        result = user_service.create_user_and_conf('test1234@test.com', 'mooo1', 'mooo1')
        self.assertEquals(User.objects.all().count(), 2)
        self.assertEquals(UserConfirmation.objects.all().count(), 1)
        self.assertEquals(result["user"].username, 'mooo1')
        self.assertEquals(len(result["conf"].confirmation_key), 64)
