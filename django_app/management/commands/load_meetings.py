''' module for the load meetings command '''
# pylint: disable=too-many-locals
import os
import logging
import json
import requests
from django.core.management.base import BaseCommand
from django_app.services.auth_service import RefererTokenSessionHelper


LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    ''' class for the command '''

    def add_arguments(self, parser):
        parser.add_argument('--meeting_file', default="/home/dtuser/Desktop/latest_meetings.txt")
        parser.add_argument('--username', default='mf_admin')
        parser.add_argument('--password', default='mf_admin')
        parser.add_argument('--base_url', default='http://127.0.0.1:8000')
        parser.add_argument('--error_file', default=os.path.join(os.path.dirname(__file__),
                                                                 '..', '..', '..', 'loader_error.txt'))
        parser.add_argument('--error_detail_file', default=os.path.join(os.path.dirname(__file__),
                                                                        '..', '..', '..', 'loader_error_detail.txt'))

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        base_url = options['base_url']
        meeting_file_path = options['meeting_file']
        error_file_path = options['error_file']
        error_detail_file_path = options['error_detail_file']
        post_meeting_url = "%s%s" % (base_url, "mfserver2/api/v1/savemeeting/")
        helper = RefererTokenSessionHelper(username, password, base_url)
        the_referer = helper.get_referer()
        the_token, session_id = helper.get_token_session()
        meeting_file_handle = open(meeting_file_path)
        cookies = dict(csrftoken=the_token, sessionid=session_id)
        headers = {"X-CSRFToken": the_token, "referer": the_referer,
                   "Content-Type": "application/json"}
        error_handle = open(error_file_path, 'w')
        error_detail_handle = open(error_detail_file_path, 'w')
        meetings_found = 0
        meetings_succeeded = 0
        for line in meeting_file_handle:
            stripped_line = line.strip()
            if stripped_line:
                meetings_found += 1
                response = None
                try:
                    meeting_obj = json.loads(line)
                    response = requests.post(post_meeting_url,
                                             json.dumps(meeting_obj),
                                             cookies=cookies,
                                             headers=headers,
                                             verify=False)
                    if response.status_code == 201:
                        meetings_succeeded += 1
                    else:
                        raise  # pylint: disable=misplaced-bare-raise
                except:  # pylint: disable=bare-except
                    error_handle.write(stripped_line + '\n')
                    error_detail_handle.write('%s\n%s\n%s\n\n' % (stripped_line,
                                                                  response.status_code if response is not None else "",
                                                                  response.text if response is not None else ""))
        meeting_file_handle.close()
        error_handle.close()
        error_detail_handle.close()
        meetings_failed = meetings_found - meetings_succeeded
        LOGGER.info("Ran %s commands, of them %s succeeded and %s failed",
                    meetings_found, meetings_succeeded, meetings_failed)
