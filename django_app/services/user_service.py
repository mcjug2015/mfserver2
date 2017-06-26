''' user services module '''
# pylint: disable=no-member
import random
import string
from django.contrib.auth.models import User
from django.utils import timezone
from django_app.models import UserConfirmation


def get_user_to_register(email):
    '''
        if no matching user exists will return an unsaved user obj
        if matching user exists but is inactive, will return that db object
        Otherwise None will be returned since registration should not go through
    '''
    retval = None
    user_query = User.objects.filter(username=email)
    if user_query.count() == 0:
        next_pk = User.objects.latest('pk').pk + 1
        user = User(pk=next_pk, username=email, email=email, first_name='NOT_SET', last_name='NOT_SET',
                    is_active=False, is_superuser=False, is_staff=False)
        retval = user
    else:
        user = user_query[0:1][0]
        if not user.is_active:
            retval = user
    return retval


def create_user_and_conf(email, password):
    ''' create an inactive user and a conf to activate him with '''
    retval = {"user": None,
              "conf": None,
              "status": "Active user with email %s already exists" % email}
    user = get_user_to_register(email)
    if not user:
        return retval
    retval["user"] = user
    retval["status"] = "confirmation emailed to %s, click the link to complete registration" % email
    user.set_password(password)
    user.save()
    user_confirmation = create_conf(user=user, conf_type="registration")
    user_confirmation.save()
    retval["conf"] = user_confirmation
    return retval


def complete_user_registration(conf_str):
    ''' set user to active if the conf str is good '''
    retval = {"status": "Confirmation ivalid, used or expired, unable to complete user registration",
              "code": 400}
    conf_query = UserConfirmation.objects.filter(confirmation_key=conf_str,
                                                 conf_type="registration",
                                                 is_confirmed=False)
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


def request_password_reset(username):
    ''' generate a conf if user is eligible to reset password '''
    retval = {"conf": None, "user": None, "status": "invalid username %s" % username}
    user = User.objects.filter(username=username)
    if user.count() == 0:
        return retval
    user = user[0:1][0]
    if not user.is_active:
        retval["status"] = "Inactive user %s ineligible to reset password" % username
        return retval
    user_confirmation = create_conf(user=user, conf_type="password_reset")
    user_confirmation.save()
    retval["conf"] = user_confirmation
    retval["user"] = user
    retval["status"] = "successful password reset request for %s" % username
    return retval


def reset_password(conf, password):
    ''' reset password or error out '''
    if conf.is_confirmed:
        return "The password reset link you clicked has already been used and can not be used again."
    conf.user.set_password(password)
    conf.user.save()
    conf.is_confirmed = True
    conf.confirmation_date = timezone.now()
    conf.save()
    return "Successfully changed password for user %s" % conf.user.username


def create_conf(user, conf_type):
    ''' create a user confirmation '''
    user_confirmation = UserConfirmation(user=user, conf_type=conf_type)
    user_confirmation.confirmation_key = ''.join([random.choice(string.digits + string.letters)
                                                  for i in range(0, 64)])  # pylint: disable=unused-variable
    return user_confirmation
