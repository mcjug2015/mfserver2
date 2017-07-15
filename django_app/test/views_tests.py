''' test module for views '''
# pylint: disable=no-member, no-self-use
import json
from django.test.testcases import TestCase
from django.contrib.auth.models import User
from mockito.mockito import unstub, when, verify
from mockito.matchers import any  # pylint: disable=redefined-builtin
from django_app import views
from django_app.models import UserConfirmation


class RegisterUserViewTests(TestCase):
    ''' tests for the register user view '''

    def setUp(self):
        ''' set up test '''
        self.result = {}
        when(views.user_service).send_email_to_user(any(), any(), any()).thenReturn(None)
        when(views.user_service).create_user_and_conf(any(), any()).thenReturn(self.result)

    def tearDown(self):
        ''' tear down test '''
        unstub()

    def test_get(self):
        ''' make sure that get with a valid confirmation param works '''
        when(views.user_service).complete_user_registration(any()).thenReturn({"code": 200,
                                                                               "status": "test"})
        response = self.client.get("/mfserver2/register/", {"confirmation": "test_conf"})
        self.assertEquals(response.status_code, 200)
        verify(views.user_service).complete_user_registration(any())

    def test_post_success(self):
        ''' test successfully registering a user '''
        self.result["user"] = User.objects.get(username="mf_admin")
        self.result["status"] = "test good status"
        self.result["conf"] = UserConfirmation(confirmation_key="testing123")
        response = self.client.post("/mfserver2/register/",
                                    content_type='application/json',
                                    data=json.dumps({"email": "mf_test@test.com",
                                                     "password": "fake123"}))
        self.assertEquals(response.status_code, 201)
        verify(views.user_service).send_email_to_user(any(), any(), any())

    def test_post_fail(self):
        ''' test registering an inelligible user '''
        self.result["user"] = None
        self.result["status"] = "test bad status"
        response = self.client.post("/mfserver2/register/",
                                    content_type='application/json',
                                    data=json.dumps({"email": "mf_test@test.com",
                                                     "password": "fake123"}))
        self.assertEquals(response.status_code, 400)
        verify(views.user_service, times=0).send_email_to_user(any(), any(), any())


class LoginAsyncTests(TestCase):
    ''' class for login_async views method '''
    fixtures = ['users_groups_perms.json']

    def test_invalid_login(self):
        ''' make sure we get 403 status code when wrong u/p is provided '''
        json_input = {'username': 'wrong', 'password': 'wrongovich'}
        response = self.client.post('/mfserver2/login_async/',
                                    content_type='application/json',
                                    data=json.dumps(json_input))
        self.assertEquals(response.status_code, 403)
        resp_obj = json.loads(response.content)
        self.assertEquals(resp_obj['status_code'], 403)
        self.assertEquals(resp_obj['status'], 'wrong u/p or inactive user')

    def test_inactive_user(self):
        ''' verify that we get a 403 when an inactive user tries to login '''
        the_user = User.objects.get(pk=1)
        the_user.is_active = False
        the_user.save()
        json_input = {'username': 'test_user', 'password': 'testing123'}
        response = self.client.post('/mfserver2/login_async/',
                                    content_type='application/json',
                                    data=json.dumps(json_input))
        self.assertEquals(response.status_code, 403)
        resp_obj = json.loads(response.content)
        self.assertEquals(resp_obj['status_code'], 403)
        self.assertEquals(resp_obj['status'], 'wrong u/p or inactive user')

    def test_success(self):
        ''' verify that we get a 200 with good creds '''
        json_input = {'username': 'test_user', 'password': 'testing123'}
        response = self.client.post('/mfserver2/login_async/',
                                    content_type='application/json',
                                    data=json.dumps(json_input))
        self.assertEquals(response.status_code, 200)
        resp_obj = json.loads(response.content)
        self.assertEquals(resp_obj['status_code'], 200)
        self.assertEquals(resp_obj['status'], 'good to go')


class LogoutAsyncTests(TestCase):
    ''' tests for the logout_async view '''
    fixtures = ['users_groups_perms.json']

    def test_success(self):
        ''' make sure logout_async truly logs the user out. '''
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 302)

        self.client.login(username='test_user', password='testing123')
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)

        response = self.client.get('/mfserver2/logout_async/')
        self.assertEquals(response.status_code, 200)
        resp_obj = json.loads(response.content)
        self.assertEquals(resp_obj['status'], 'logout success')

        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 302)


class IndexViewTests(TestCase):
    ''' test class for the index view '''

    def test_get(self):
        ''' test accessing the index view '''
        response = self.client.get('/mfserver2/welcome/')
        self.assertEquals(response.status_code, 200)
        self.assertIn("Welcome to meeting finder server 2", response.content)


class ChangePasswordViewTests(TestCase):
    ''' tests for the change password view '''
    fixtures = ['users_groups_perms.json']

    def test_wrong_old_password(self):
        ''' make sure we get 401 when incorrect old password is sent in '''
        self.client.login(username='test_user', password='testing123')
        response = self.client.post("/mfserver2/change_password/",
                                    content_type='application/json',
                                    data=json.dumps({'old_password': "wrong",
                                                     'new_password': "irrelevant"}))
        self.assertEquals(response.status_code, 401)

    def test_success(self):
        ''' make sure successful password change logs user out '''
        self.client.login(username='test_user', password='testing123')
        response = self.client.post("/mfserver2/change_password/",
                                    content_type='application/json',
                                    data=json.dumps({'old_password': "testing123",
                                                     'new_password': "1234abcd"}))
        self.assertEquals(response.status_code, 200)
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 302)
        self.client.login(username='test_user', password='1234abcd')
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)


class RequestResetPasswordTests(TestCase):
    ''' tests for the RequestResetPassword view '''

    def setUp(self):
        ''' set up test '''
        self.result = {}
        when(views.user_service).send_email_to_user(any(), any(), any()).thenReturn(None)
        when(views.user_service).request_password_reset(any()).thenReturn(self.result)

    def tearDown(self):
        ''' tear down test '''
        unstub()

    def test_get_fail(self):
        ''' http forbidden if conf with given key not found '''
        response = self.client.get("/mfserver2/reset_password_request/",
                                   {"confirmation": "i_do_not_exist"})
        self.assertEquals(response.status_code, 403)

    def test_get_success(self):
        ''' make sure view with username name confirmation key gets returned on get '''
        user = User.objects.get(username="mf_admin")
        user_conf = UserConfirmation(confirmation_key="testing456", user=user,
                                     conf_type="password_reset")
        user_conf.save()
        response = self.client.get("/mfserver2/reset_password_request/",
                                   {"confirmation": "testing456"})
        self.assertEquals(response.status_code, 200)
        self.assertIn("Reset password for mf_admin", response.content)
        self.assertIn("testing456", response.content)
        self.assertNotIn("Passwords did not match", response.content)
        self.assertNotIn("Password must be longer than 6 characters", response.content)

    def test_post_fail(self):
        ''' 400 returned when user service does not create conf '''
        self.result["conf"] = None
        self.result["status"] = "test fail status"
        response = self.client.post("/mfserver2/reset_password_request/",
                                    content_type='application/json',
                                    data=json.dumps({"email": "mf_test@test.com"}))
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.content, "test fail status")
        verify(views.user_service, times=0).send_email_to_user(any(), any(), any())

    def test_post_success(self):
        ''' 200 returned, send email invoked when user service succeeds '''
        self.result["user"] = User.objects.get(username="mf_admin")
        self.result["conf"] = UserConfirmation(confirmation_key="testing123")
        response = self.client.post("/mfserver2/reset_password_request/",
                                    content_type='application/json',
                                    data=json.dumps({"email": "mf_test@test.com"}))
        self.assertEquals(response.status_code, 200)
        self.assertIn("Emailed password reset link", response.content)
        verify(views.user_service, times=1).send_email_to_user(any(), any(), any())


class ResetPasswordTests(TestCase):
    ''' tests for the reset password view '''

    def setUp(self):
        ''' set up test '''
        self.user = User.objects.get(username="mf_admin")
        UserConfirmation(confirmation_key="testing456", user=self.user,
                         conf_type="password_reset").save()

    def tearDown(self):
        ''' tear down test '''
        unstub()

    def test_no_such_conf(self):
        ''' http forbidden if conf not found '''
        response = self.client.post("/mfserver2/reset_password/",
                                    data={"reset_conf": "i_do_not_exist"})
        self.assertEquals(response.status_code, 403)

    def test_invalid_password(self):
        ''' page with error message when passwords not matching or less than 6 characters '''
        response = self.client.post("/mfserver2/reset_password/",
                                    data={"reset_conf": "testing456",
                                          "password": "abc",
                                          "retype_password": "123"})
        self.assertEquals(response.status_code, 200)
        self.assertIn("Passwords did not match", response.content)
        self.assertIn("Password must be longer than 6 characters", response.content)

    def test_fail_service(self):
        ''' service failing causes http 400 '''
        when(views.user_service).reset_password(any(), any()).thenReturn("fail")
        response = self.client.post("/mfserver2/reset_password/",
                                    data={"reset_conf": "testing456",
                                          "password": "abc123",
                                          "retype_password": "abc123"})
        self.assertEquals(response.status_code, 400)
        self.assertIn("fail", response.content)

    def test_success(self):
        ''' service success causes http 200 '''
        when(views.user_service).reset_password(any(), any()).thenReturn("Successfully")
        response = self.client.post("/mfserver2/reset_password/",
                                    data={"reset_conf": "testing456",
                                          "password": "abc123",
                                          "retype_password": "abc123"})
        self.assertEquals(response.status_code, 200)
        self.assertIn("Successfully", response.content)
