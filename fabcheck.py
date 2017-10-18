import os
import sys
from fabric.api import env, local
from django_app.services.request_service import create_user
from django_app.services.auth_service import RefererTokenSessionHelper


env.base_url = "https://138.197.14.186"
env.admin_username = "mf_admin"
env.admin_password = "mf_admin"
env.temp_user_obj = {"username": "temp_user_deleteme",
                     "is_active": True,
                     "is_staff": False,
                     "last_login": '2017-10-18 02:16:38.106658+00:00',
                     "email": "fake_email@test.com",
                     "date_joined": '2017-10-18 02:16:38.106658+00:00',
                     "password": "The_fakeP@ssword"}


def _ensure_virtualenv():
    if "VIRTUAL_ENV" not in os.environ:
        sys.stderr.write("$VIRTUAL_ENV not found. Make sure to activate virtualenv first\n\n")
        sys.exit(-1)
    env.virtualenv = os.environ["VIRTUAL_ENV"]


def are_we_cool_yet():
    helper = RefererTokenSessionHelper(env.admin_username, env.admin_password, env.base_url)
    the_referer = helper.get_referer()
    the_token1, session_id = helper.get_token_session()
    create_user(env.temp_user_obj, env.base_url, the_referer, the_token1, session_id)
