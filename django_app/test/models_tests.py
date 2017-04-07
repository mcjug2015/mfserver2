''' test module for models '''
from django.test.testcases import TestCase
from django.utils.dateparse import parse_datetime
from django.contrib.auth.models import User
from django_app.models import MeetingType, UserConfirmation, Meeting


class StrReprTests(TestCase):
    ''' tests for the __str__ methods of various models '''

    def test_str(self):
        ''' test the str methods '''
        the_date = parse_datetime("2012-02-21 10:28:45")
        user = User(username="test user")
        conf = UserConfirmation(expiration_date=the_date,
                                conf_type="test type",
                                user=user)
        self.assertEquals(str(conf), "2012-02-21 10:28 test type(test user)")
        self.assertEquals(str(MeetingType(name="qq", short_name="q")), "q(qq)")
        meeting = Meeting(name="a", creator=user)
        self.assertEquals(str(meeting), "a(test user)")
