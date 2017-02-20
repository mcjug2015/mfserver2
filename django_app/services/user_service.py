''' user services module '''
import datetime
import random
import string
from django.contrib.auth.models import User
from django.utils import timezone
from django_app.models import UserConfirmation


def create_user_and_conf(email, username, password):
    ''' create an inactive user and a conf to activate him with '''
    user = User(username=username, email=email, first_name='NOT_SET', last_name='NOT_SET', is_active=False,
                is_superuser=False, is_staff=False)
    user.set_password(password)
    user.save()
    user_confirmation = UserConfirmation(user=user)
    user_confirmation.expiration_date = timezone.now() + datetime.timedelta(days=3)
    user_confirmation.confirmation_key = ''.join([random.choice(string.digits + string.letters)
                                                  for i in range(0, 64)])  # pylint: disable=unused-variable
    user_confirmation.save()
    return user, user_confirmation
