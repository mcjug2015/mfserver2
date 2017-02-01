''' tests for the api module '''
# pylint: disable=no-member, protected-access
from django.test.testcases import TestCase
from tastypie.exceptions import NotFound
from django_app.api import ExceptionThrowingModelResource


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
