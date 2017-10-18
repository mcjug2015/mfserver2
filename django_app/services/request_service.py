''' various useful requests '''
import requests


def create_user(user_obj, base_url, referer, token, session_id):
    ''' create a user via admin request '''
    response = requests.post("%s/mfserver2/admin_api/v1/admin_user/" % base_url,
                             json=user_obj,
                             headers={"X-CSRFToken": token,
                                      "referer": referer},
                             cookies={"csrftoken": token,
                                      "sessionid": session_id},
                             verify=False)
    response.raise_for_status()
