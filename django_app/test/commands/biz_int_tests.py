''' tests for the biz_int command module '''
# pylint: disable=no-self-use
from django.test.testcases import TestCase
from mockito.mockito import when, verify
from django_app.management.commands import biz_int


class BizIntTests(TestCase):
    ''' tests for the command class '''

    def test_handle(self):
        ''' test the handle method '''
        when(biz_int.driver).drive().thenReturn(None)
        biz_int.Command().handle()
        verify(biz_int.driver).drive()
