''' tests for the api module '''
# pylint: disable=no-member, protected-access
from django.test.testcases import TestCase
from tastypie.exceptions import NotFound
from django_app.api import ExceptionThrowingModelResource, SaveMeetingResource
from django_app.models import Meeting
from mockito.mocking import mock


class SaveMeetingTests(TestCase):
    ''' test the custom savemeeting method '''

    def test_save(self):
        ''' test for the custom savemeeting method '''
        bundle = mock()
        bundle.data = {'geo_location': {'coordinates': [-76, 35]}}
        bundle.obj = Meeting()
        retval = SaveMeetingResource().save(bundle)
        self.assertIsNotNone(retval)


class ExceptionThrowingModelResourceTests(TestCase):
    ''' unit tests for the ExceptionThrowingModelResource '''

    def test_real_error(self):
        ''' make sure a real error gets raised '''
        exception = ValueError("testing123")
        self.assertRaises(ValueError, ExceptionThrowingModelResource()._handle_500,
                          None, exception)

    def test_not_found(self):
        ''' make sure a not found exceptions results in a not found response '''
        exception = NotFound()
        response = ExceptionThrowingModelResource()._handle_500(None, exception)
        self.assertTrue(response.status_code, 404)
