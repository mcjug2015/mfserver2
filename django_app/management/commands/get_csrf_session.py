''' module for command that turns username and password into csrf and sessionid cookie '''
from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup


class Command(BaseCommand):
    ''' class for the command '''

    def add_arguments(self, parser):
        parser.add_argument('--username', default='admin')
        parser.add_argument('--password', default='admin')
        parser.add_argument('--initial_url', default='http://localhost:8000/mfserver2/welcome/')
        parser.add_argument('--login_url', default='http://127.0.0.1:8000/mfserver2/login_async/')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        initial_url = options['initial_url']
        login_url = options['login_url']
        response = requests.get(initial_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        the_token = soup.find_all('input')[0].attrs['value']
        the_cookie = response.cookies['csrftoken']
        headers = {'Content-Type': 'application/json',
                   'X-CSRFToken': the_token}
        cookies = dict(csrftoken=the_cookie)
        response = requests.post(login_url, headers=headers, cookies=cookies,
                                 json={'username': username, 'password': password})
        latest_csrf_cookie = response.cookies['csrftoken']
        session_id = response.cookies['sessionid']
        print 'curl -f -k -v --cookie "csrftoken=%s" --cookie "sessionid=%s"' % (latest_csrf_cookie,
                                                                                 session_id)
