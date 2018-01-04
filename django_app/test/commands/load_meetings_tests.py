''' tests module for the load meetings command '''
from tempfile import mkdtemp
import shutil
import os
from django.test.testcases import TestCase
from mockito.mockito import unstub, verify, when
from mockito.matchers import any  # pylint: disable=redefined-builtin
from mockito.mocking import mock
from django_app.management.commands import load_meetings


class LoadMeetingsTests(TestCase):
    ''' test class for the load meetings command '''

    def setUp(self):
        ''' set up the test '''
        self.work_dir = mkdtemp()
        self.command = load_meetings.Command()

    def tearDown(self):
        ''' tear down test '''
        unstub()
        shutil.rmtree(self.work_dir)

    def test_add_arguments(self):
        ''' test adding arguements '''
        the_parser = mock()
        when(the_parser).add_argument(any(), default=any()).thenReturn(None)
        self.command.add_arguments(the_parser)
        verify(the_parser, times=6).add_argument(any(), default=any())

    def test_handle(self):
        ''' verify that good and failing meetings act appropriately '''
        when(load_meetings.RefererTokenSessionHelper).get_referer().thenReturn("test_referer")
        when(load_meetings.RefererTokenSessionHelper).get_token_session().thenReturn(("test_token",
                                                                                      "test_session"))
        meeting_file_path = os.path.join(os.path.dirname(__file__), '..', 'res', 'test_meetings_to_load.txt')
        error_file_path = os.path.join(self.work_dir, "test_error.txt")
        error_detail_file_path = os.path.join(self.work_dir, "test_error_detail.txt")
        response1 = mock()
        response1.status_code = 201
        response2 = mock()
        response2.status_code = 500
        response2.text = "test fail response text"
        when(load_meetings.requests).post(any(), any(), cookies=any(),
                                          headers=any(), verify=False).thenReturn(response1, response2)
        self.command.handle(username="a", password="b", base_url="c",
                            meeting_file=meeting_file_path,
                            error_file=error_file_path,
                            error_detail_file=error_detail_file_path)
        error_output = open(error_file_path).read()
        error_detail_output = open(error_detail_file_path).read()
        verify(load_meetings.RefererTokenSessionHelper).get_referer()
        verify(load_meetings.RefererTokenSessionHelper).get_token_session()
        verify(load_meetings.requests, times=2).post(any(), any(), cookies=any(), headers=any(),
                                                     verify=False)
        self.assertIn("-777777777.0", error_output)
        self.assertIn("zzzzz", error_output)
        self.assertIn("-777777777.0", error_detail_output)
        self.assertIn("500", error_detail_output)
        self.assertIn("test fail response text", error_detail_output)
        self.assertIn("zzzzz", error_detail_output)
