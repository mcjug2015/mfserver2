''' module for command that turns username and password into csrf and sessionid cookie '''
from django.core.management.base import BaseCommand
from django_app.services.auth_service import RefererTokenSessionHelper


class Command(BaseCommand):
    ''' class for the command '''

    def add_arguments(self, parser):
        parser.add_argument('--username', default='mf_admin')
        parser.add_argument('--password', default='mf_admin')
        parser.add_argument('--initial_url', default='http://127.0.0.1:8000/mfserver2/welcome/')
        parser.add_argument('--login_url', default='http://127.0.0.1:8000/mfserver2/login_async/')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        initial_url = options['initial_url']
        login_url = options['login_url']
        helper = RefererTokenSessionHelper(username, password,
                                           initial_url, login_url)
        the_referer = helper.get_referer()
        the_token1, session_id = helper.get_token_session()
        retval = 'curl -f -k -v --cookie "csrftoken=%s;sessionid=%s"' % (the_token1,
                                                                         session_id)
        retval += ' -H "X-CSRFToken: %s" -H "referer: %s"' % (the_token1,
                                                              the_referer)
        return retval
