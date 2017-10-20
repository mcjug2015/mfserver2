''' various useful requests '''
# pylint: disable=too-many-arguments
import logging
import requests
LOGGER = logging.getLogger(__name__)


def create_user(user_obj, base_url, referer, token, session_id):
    ''' create a user via admin request '''
    response = do_http_method(requests.post,
                              "%s/mfserver2/admin_api/v1/admin_user/" % base_url,
                              referer, token, session_id, user_obj)
    return response.json()['resource_uri']


def create_meeting(meeting_obj, base_url, referer, token, session_id):
    ''' create a meeting via admin request '''
    response = do_http_method(requests.post,
                              "%s/mfserver2/api/v1/savemeeting/" % base_url,
                              referer, token, session_id, meeting_obj)
    return response.json()['resource_uri']


def delete_user(user_uri, base_url, referer, token, session_id):
    ''' delete user at uri '''
    do_http_method(requests.delete,
                   "%s%s" % (base_url, user_uri),
                   referer, token, session_id)


def do_http_method(the_method, url, referer, token, session_id, json_obj=None):
    ''' execute https method with supplied request params '''
    headers = {"X-CSRFToken": token,
               "referer": referer}
    cookies = {"csrftoken": token,
               "sessionid": session_id}
    if json_obj:
        response = the_method(url, json=json_obj, headers=headers,
                              cookies=cookies, verify=False)
    else:
        response = the_method(url, headers=headers,
                              cookies=cookies, verify=False)
    response.raise_for_status()
    return response
