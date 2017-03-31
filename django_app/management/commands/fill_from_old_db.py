''' invokes commands to fill current mfserver2 db from old aabuddy db '''
from django.core.management.base import BaseCommand
from django_app.old_db_restore import converter
from django_app.old_db_restore.converter import MeetingTypeConverter


class Command(BaseCommand):
    ''' command wrapper '''

    def handle(self, *args, **options):
        conn = converter.get_conn()
        MeetingTypeConverter.convert(conn)
