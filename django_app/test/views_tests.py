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
        when(views).send_email_to_user(any(), any(), any()).thenReturn(None)
        when(views.user_service).create_user_and_conf(any(), any(), any()).thenReturn(self.result)

    def tearDown(self):
        ''' tear down test '''
        unstub()

    def test_success(self):
        ''' test successfully registering a user '''
        self.result["user"] = User.objects.get(username="admin")
        self.result["status"] = "test good status"
        self.result["conf"] = UserConfirmation(confirmation_key="testing123")
        response = self.client.post("/mfserver2/register/",
                                    content_type='application/json',
                                    data=json.dumps({"email": "test@test.com",
                                                     "password": "fake123"}))
        self.assertEquals(response.status_code, 201)
        verify(views).send_email_to_user(any(), any(), any())

    def test_fail(self):
        ''' test registering an inelligible user '''
        self.result["user"] = None
        self.result["status"] = "test bad status"
        response = self.client.post("/mfserver2/register/",
                                    content_type='application/json',
                                    data=json.dumps({"email": "test@test.com",
                                                     "password": "fake123"}))
        self.assertEquals(response.status_code, 400)
        verify(views, times=0).send_email_to_user(any(), any(), any())


class LoginAsyncTests(TestCase):
    ''' class for login_async views method '''
    fixtures = ['users_groups_perms.json']

    def test_invalid_login(self):
        ''' make sure we get 403 status code when wrong u/p is provided '''
        json_input = {'username': 'wrong', 'password': 'wrongovich'}
        response = self.client.post('/mfserver2/login_async/',
                                    content_type='application/json',
                                    data=json.dumps(json_input))
        self.assertEquals(response.status_code, 200)
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
        self.assertEquals(response.status_code, 200)
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


class SendEmailToUserTest(TestCase):
    ''' test send_email_to_user method with mocks '''

    def tearDown(self):
        ''' tear down test '''
        unstub()

    def test_send_email(self):
        ''' test sending email to user '''
        when(views.django_mail).send_mail(subject=any(), message=any(),
                                          from_email=any(),
                                          recipient_list=any(),
                                          fail_silently=any()).thenReturn(None)
        views.send_email_to_user(User.objects.get(username="admin"), "a", "b")
        verify(views.django_mail).send_mail(subject=any(), message=any(),
                                            from_email=any(),
                                            recipient_list=any(),
                                            fail_silently=any())
