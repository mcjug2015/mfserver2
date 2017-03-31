''' uses old aabuddy db to safely fill mfserver2 db '''
# pylint: disable=no-member,too-few-public-methods
import psycopg2
from django_app.models import MeetingType


def get_conn(db_host="127.0.0.1", db_port="5432", db_username="mfserver2",
             db_password="mfserver2", db_name="old_aabuddy"):
    ''' get conn for old database '''
    return psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s' port='%s'" % (db_name,
                                                                                         db_username,
                                                                                         db_host,
                                                                                         db_password,
                                                                                         db_port))


class MeetingTypeConverter(object):
    ''' grabs old meeting types and loads them into mfserver2 '''

    @classmethod
    def convert(cls, conn):
        ''' copy from old db to new '''
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("""select id, short_name, name, description from aabuddy_meetingtype""")
        old_meeting_types = cursor.fetchall()
        for meeting_type in old_meeting_types:
            MeetingType.objects.get_or_create(pk=meeting_type['id'],
                                              short_name=meeting_type['short_name'],
                                              name=meeting_type['name'],
                                              description=meeting_type['description'])
