''' tests module for user_service '''
# pylint: disable=no-member, no-self-use
from django.test.testcases import TestCase
from django.contrib.auth.models import User
from mockito.mockito import when, unstub, verify
from mockito.matchers import any  # pylint: disable=redefined-builtin
from django_app.models import UserConfirmation
from django_app.services import user_service


class GetUserToRegisterTests(TestCase):
    ''' tests for the get user to register method '''

    def test_existing_user_fail(self):
        ''' make sure active existing user is not elligible to register '''
        result = user_service.get_user_to_register("mf_admin")
        self.assertIsNone(result)

    def test_existing_user_success(self):
        ''' make sure existing user with unconfirmed, expired conf can register '''
        user = User.objects.get(email="mf_test@test.com")
        user.is_active = False
        user.save()
        result = user_service.get_user_to_register("mf_admin")
        self.assertEqual(result.username, "mf_admin")

    def test_new_user(self):
        ''' test getting a new user back '''
        result = user_service.get_user_to_register("test@mooo.com")
        self.assertEqual(result.email, "test@mooo.com")


class CreateUserAnConfTests(TestCase):
    ''' test class for the create_user_and_conf method '''

    def tearDown(self):
        ''' tear down test '''
        unstub()

    def test_no_user(self):
        ''' make sure nothing happens if user should not be registered '''
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(UserConfirmation.objects.all().count(), 0)
        when(user_service).get_user_to_register(any()).thenReturn(None)
        result = user_service.create_user_and_conf('test1234@test.com', 'mooo1')
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(UserConfirmation.objects.all().count(), 0)
        self.assertEqual(result["status"], "Active user with email test1234@test.com already exists")

    def test_success(self):
        ''' make sure method successfully creates user and conf '''
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(UserConfirmation.objects.all().count(), 0)
        user = User(pk=1000, username='test1234@test.com', email='test1234@test.com',
                    first_name='NOT_SET', last_name='NOT_SET',
                    is_active=False, is_superuser=False, is_staff=False)
        when(user_service).get_user_to_register(any()).thenReturn(user)
        result = user_service.create_user_and_conf('test1234@test.com', 'mooo1')
        self.assertEqual(User.objects.all().count(), 2)
        self.assertEqual(UserConfirmation.objects.all().count(), 1)
        self.assertEqual(result["user"].username, 'test1234@test.com')
        self.assertEqual(len(result["conf"].confirmation_key), 64)
        self.assertEqual(result["conf"].conf_type, "registration")


class CompleteUserRegistration(TestCase):
    ''' tests for the complete user registration method '''

    def setUp(self):
        ''' set up tests '''
        User.objects.all().update(is_active=False)

    def test_fail_no_conf(self):
        ''' make sure method fails if no conf exists with the str passed in '''
        result = user_service.complete_user_registration("wrong")
        self.assertEqual(result["status"],
                         "Confirmation ivalid, used or expired, unable to complete user registration")
        self.assertEqual(User.objects.filter(is_active=True).count(), 0)

    def test_success(self):
        ''' test successfull registration completion '''
        user = User.objects.get(username="mf_admin")
        user_confirmation = UserConfirmation(user=user, conf_type="registration")
        user_confirmation.confirmation_key = "right"
        user_confirmation.save()
        result = user_service.complete_user_registration("right")
        self.assertIn("Successfully completed registration for", result["status"])
        self.assertEqual(User.objects.filter(is_active=True).count(), 1)


class RequestPasswordResetTests(TestCase):
    ''' tests for the request_password_reset method '''

    def test_no_such_user(self):
        ''' appropriate status returned when no user exists '''
        retval = user_service.request_password_reset("i do not exist")
        self.assertIsNone(retval["conf"])
        self.assertIn("invalid username", retval["status"])

    def test_inactive_user(self):
        ''' no reset for inactive user '''
        user = User.objects.get(username="mf_admin")
        user.is_active = False
        user.save()
        retval = user_service.request_password_reset("mf_admin")
        self.assertIsNone(retval["conf"])
        self.assertIn("Inactive user", retval["status"])

    def test_success(self):
        ''' existing, active user able to get reset password conf '''
        retval = user_service.request_password_reset("mf_admin")
        self.assertEqual(retval["conf"].user.username, "mf_admin")
        self.assertEqual(User.objects.get(username="mf_admin").confirmations.all()[0:1][0].conf_type, "password_reset")
        self.assertIn("successful password reset", retval["status"])


class ResetPasswordTests(TestCase):
    ''' tests for the reset password method '''

    def test_is_confirmed(self):
        ''' error message if conf has already been confirmed '''
        retval = user_service.reset_password(UserConfirmation(is_confirmed=True), "irrelevant")
        self.assertIn("has already been used", retval)

    def test_success(self):
        ''' test successfully resetting password '''
        user = User.objects.get(username="mf_admin")
        user_confirmation = UserConfirmation(user=user, conf_type="reset_password")
        user_confirmation.confirmation_key = "right"
        user_confirmation.save()
        retval = user_service.reset_password(user_confirmation, "test_password123")
        self.assertIn("Successfully changed password", retval)
        self.assertTrue(user_confirmation.is_confirmed)
        self.assertTrue(User.objects.get(username="mf_admin").check_password("test_password123"))


class SendEmailToUserTest(TestCase):
    ''' test send_email_to_user method with mocks '''

    def tearDown(self):
        ''' tear down test '''
        unstub()

    def test_send_email(self):
        ''' test sending email to user '''
        when(user_service.django_mail).send_mail(subject=any(), message=any(),
                                                 from_email=any(),
                                                 recipient_list=any(),
                                                 fail_silently=any()).thenReturn(None)
        user_service.send_email_to_user(User.objects.get(username="mf_admin"), "a", "b")
        verify(user_service.django_mail).send_mail(subject=any(), message=any(),
                                                   from_email=any(),
                                                   recipient_list=any(),
                                                   fail_silently=any())
