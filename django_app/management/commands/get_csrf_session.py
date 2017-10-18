''' module for command that turns username and password into csrf and sessionid cookie '''
from django.core.management.base import BaseCommand
from django_app.services.auth_service import RefererTokenSessionHelper


class Command(BaseCommand):
    ''' class for the command '''

    def add_arguments(self, parser):
        parser.add_argument('--username', default='mf_admin')
        parser.add_argument('--password', default='mf_admin')
        parser.add_argument('--base_url', default='http://127.0.0.1:8000')

    def handle(self, *args, **options):
        helper = RefererTokenSessionHelper(options['username'], options['password'],
                                           options['base_url'])
        the_referer = helper.get_referer()
        the_token1, session_id = helper.get_token_session()
        retval = 'curl -f -k -v --cookie "csrftoken=%s;sessionid=%s"' % (the_token1,
                                                                         session_id)
        retval += ' -H "X-CSRFToken: %s" -H "referer: %s"' % (the_token1,
                                                              the_referer)
        return retval
