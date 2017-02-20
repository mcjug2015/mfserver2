''' tests module for user_service '''
# pylint: disable=no-member
from django.test.testcases import TestCase
from django.contrib.auth.models import User
from django_app.models import UserConfirmation
from django_app.services import user_service


class CreateUserAnConfTests(TestCase):
    ''' test class for the create_user_and_conf method '''

    def test_success(self):
        ''' make sure method successfully creates user and conf '''
        self.assertEquals(User.objects.all().count(), 1)
        self.assertEquals(UserConfirmation.objects.all().count(), 0)
        user, conf = user_service.create_user_and_conf('test1234@test.com', 'mooo1', 'mooo1')
        self.assertEquals(User.objects.all().count(), 2)
        self.assertEquals(UserConfirmation.objects.all().count(), 1)
        self.assertEquals(user.username, 'mooo1')
        self.assertEquals(len(conf.confirmation_key), 64)
