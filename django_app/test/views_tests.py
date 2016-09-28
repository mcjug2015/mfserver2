''' test module for views '''
# pylint: disable=no-member
from django.test.testcases import TestCase


class IndexViewTests(TestCase):
    ''' test class for the index view '''

    def test_get(self):
        ''' test accessing the index view '''
        response = self.client.get('/mfserver2/welcome/')
        self.assertEquals(response.status_code, 200)
        self.assertIn("Welcome to meeting finder server 2", response.content)
