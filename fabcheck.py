import os
import sys
from fabric.api import env, local
from django_app.services.request_service import create_user, create_meeting,\
    delete_user
from django_app.services.auth_service import RefererTokenSessionHelper


env.base_url = "https://127.0.0.1"
env.admin_username = "mf_admin"
env.admin_password = "mf_admin"
env.temp_user_obj = {"username": "temp_user_deleteme",
                     "is_active": True,
                     "is_staff": False,
                     "last_login": '2017-10-18 02:16:38.106658+00:00',
                     "email": "fake_email@test.com",
                     "date_joined": '2017-10-18 02:16:38.106658+00:00',
                     "password": "The_fakeP@ssword"}
env.temp_meeting_obj = {"geo_location": {"coordinates": ['22.0', '24.0'], "type": "Point"},
                        "name": "temp meeting delete",
                        "day_of_week": 3,
                        "start_time": "17:30",
                        "end_time": "18:30",
                        "description": "temp meeting that should be deleted",
                        "address": "fake address for temp meeting",
                        "is_active": True,
                        "types": []}


def _ensure_virtualenv():
    if "VIRTUAL_ENV" not in os.environ:
        sys.stderr.write("$VIRTUAL_ENV not found. Make sure to activate virtualenv first\n\n")
        sys.exit(-1)
    env.virtualenv = os.environ["VIRTUAL_ENV"]


def are_we_cool_yet():
    helper = RefererTokenSessionHelper(env.admin_username, env.admin_password, env.base_url)
    the_referer = helper.get_referer()
    the_token1, session_id = helper.get_token_session()
    user_uri = create_user(env.temp_user_obj, env.base_url, the_referer, the_token1, session_id)
    
    helper = RefererTokenSessionHelper(env.temp_user_obj['username'],
                                       env.temp_user_obj['password'],
                                       env.base_url)
    user_referer = helper.get_referer()
    user_token, user_session_id = helper.get_token_session()
    meeting_uri = create_meeting(env.temp_meeting_obj, env.base_url, user_referer,
                                 user_token, user_session_id)
    delete_user(user_uri, env.base_url, the_referer, the_token1, session_id)
    pass
