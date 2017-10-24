''' command to invoke biz int driver '''
from django.core.management.base import BaseCommand
from biz_int import driver


class Command(BaseCommand):
    ''' command wrapper '''

    def handle(self, *args, **options):
        driver.drive()
