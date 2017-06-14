''' service module for auth related stuff '''
from urlparse import urlparse
import requests
from bs4 import BeautifulSoup


class RefererTokenSessionHelper(object):
    ''' gets csrf and session id from mfserver2 instances '''

    def __init__(self, username, password, initial_url, login_url):
        self.username = username
        self.password = password
        self.initial_url = initial_url
        self.login_url = login_url

    def get_referer(self):
        ''' get the referer based on initial url '''
        referer_obj = urlparse(self.initial_url)
        return '%s://%s' % (referer_obj.scheme, referer_obj.netloc)

    def get_token_session(self):
        ''' does the auth handshake, returns session and token '''
        the_referer = self.get_referer()
        response = requests.get(self.initial_url, verify=False)
        the_token1 = BeautifulSoup(response.text, 'html.parser').find_all('input')[0].attrs['value']
        the_cookie1 = response.cookies['csrftoken']
        cookies = dict(csrftoken=the_cookie1)
        response = requests.post(self.login_url,
                                 headers={'Content-Type': 'application/json',
                                          'X-CSRFToken': the_token1,
                                          'referer': the_referer},
                                 cookies=cookies,
                                 json={'username': self.username,
                                       'password': self.password},
                                 verify=False)
        session_id = response.cookies['sessionid']
        return the_token1, session_id
