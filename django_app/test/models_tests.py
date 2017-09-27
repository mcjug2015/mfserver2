''' test module for models '''
from django.test.testcases import TestCase
from django.contrib.auth.models import User
from django_app.models import MeetingType, UserConfirmation, Meeting,\
    MeetingNotThere


class StrReprTests(TestCase):
    ''' tests for the __str__ methods of various models '''

    def test_str(self):
        ''' test the str methods '''
        user = User(username="test user")
        conf = UserConfirmation(conf_type="test type",
                                user=user)
        self.assertEqual(str(conf), "test type(test user)")
        self.assertEqual(str(MeetingType(name="qq", short_name="q")), "q(qq)")
        meeting = Meeting(name="a", creator=user)
        self.assertEqual(str(meeting), "a(test user)")
        not_there = MeetingNotThere(pk=7, request_host="7")
        self.assertEqual(str(not_there), "7, host: 7")
