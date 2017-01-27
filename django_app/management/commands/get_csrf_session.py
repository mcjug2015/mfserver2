''' module for command that turns username and password into csrf and sessionid cookie '''
from urlparse import urlparse
from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup


class Command(BaseCommand):
    ''' class for the command '''

    def add_arguments(self, parser):
        parser.add_argument('--username', default='admin')
        parser.add_argument('--password', default='admin')
        parser.add_argument('--initial_url', default='http://127.0.0.1:8000/mfserver2/welcome/')
        parser.add_argument('--login_url', default='http://127.0.0.1:8000/mfserver2/login_async/')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        initial_url = options['initial_url']
        login_url = options['login_url']
        referer_obj = urlparse(initial_url)
        the_referer = '%s://%s' % (referer_obj.scheme, referer_obj.netloc)
        response = requests.get(initial_url, verify=False)
        the_token1 = BeautifulSoup(response.text, 'html.parser').find_all('input')[0].attrs['value']
        the_cookie1 = response.cookies['csrftoken']
        cookies = dict(csrftoken=the_cookie1)
        response = requests.post(login_url,
                                 headers={'Content-Type': 'application/json',
                                          'X-CSRFToken': the_token1,
                                          'referer': the_referer},
                                 cookies=cookies,
                                 json={'username': username, 'password': password},
                                 verify=False)
        session_id = response.cookies['sessionid']
        retval = 'curl -f -k -v --cookie "csrftoken=%s;sessionid=%s"' % (the_token1,
                                                                         session_id)
        retval += ' -H "X-CSRFToken: %s" -H "referer: %s"' % (the_token1,
                                                              the_referer)
        cookies = dict(csrftoken=the_token1, sessionid=session_id)
        return retval
