''' user services module '''
# pylint: disable=no-member
import datetime
import random
import string
from django.contrib.auth.models import User
from django.utils import timezone
from django_app.models import UserConfirmation


def get_user_to_register(email, username):
    '''
        if no matching user exists will return an unsaved user obj
        if matching user exists, is inactive and has an expired unconfirmed conf
            that user will be returned
        in all other cases None will be returned since registration should not go through
    '''
    retval = {"user": None,
              "status": ""}
    user_query = User.objects.filter(email=email, username=username)
    if user_query.count() == 0:
        next_pk = User.objects.latest('pk').pk + 1
        user = User(pk=next_pk, username=username, email=email, first_name='NOT_SET', last_name='NOT_SET',
                    is_active=False, is_superuser=False, is_staff=False)
        retval["user"] = user
        retval["status"] = "brand new user %s" % username
        return retval
    user = user_query[0:1][0]
    conf_query = user.confirmations.filter(is_confirmed=False, expiration_date__lt=timezone.now())
    if not user.is_active and conf_query.count() > 0:
        retval["user"] = user
        retval["status"] = "inactive user %s with expired, unconfirmed conf" % username
        return retval
    retval["status"] = "registration should not proceed for %s. is_active: %s; loose conf #%s" % (username,
                                                                                                  user.is_active,
                                                                                                  conf_query.count())
    return retval


def create_user_and_conf(email, username, password):
    ''' create an inactive user and a conf to activate him with '''
    user_dict = get_user_to_register(email, username)
    user = user_dict["user"]
    if not user:
        return user_dict
    user.set_password(password)
    user.save()
    user_confirmation = UserConfirmation(user=user)
    user_confirmation.expiration_date = timezone.now() + datetime.timedelta(days=3)
    user_confirmation.confirmation_key = ''.join([random.choice(string.digits + string.letters)
                                                  for i in range(0, 64)])  # pylint: disable=unused-variable
    user_confirmation.save()
    user_dict["conf"] = user_confirmation
    return user_dict


def complete_user_registration(conf_str):
    ''' set user to active if the conf str is good '''
    retval = {"status": "Confirmation ivalid or expired, unable to complete user registration",
              "code": 400}
    conf_query = UserConfirmation.objects.filter(confirmation_key=conf_str,
                                                 is_confirmed=False,
                                                 expiration_date__gt=timezone.now())
    if conf_query.count() == 0:
        return retval
    conf = conf_query[0:1][0]
    conf.is_confirmed = True
    conf.confirmation_date = timezone.now()
    conf.save()
    conf.user.is_active = True
    conf.user.save()
    retval["status"] = "Successfully completed registration for %s" % conf.user.username
    retval["code"] = 200
    return retval
