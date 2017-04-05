''' uses old aabuddy db to safely fill mfserver2 db '''
# pylint: disable=no-member,too-few-public-methods
import psycopg2
from django.contrib.auth.models import User
from django.contrib.gis.geos.geometry import GEOSGeometry
from django_app.models import MeetingType, Meeting


def get_conn(db_host="127.0.0.1", db_port="5432", db_username="mfserver2",
             db_password="mfserver2", db_name="old_aabuddy"):
    ''' get conn for old database '''
    return psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s' port='%s'" % (db_name,
                                                                                         db_username,
                                                                                         db_host,
                                                                                         db_password,
                                                                                         db_port))


class ConverterDriver(object):
    ''' runs the converters '''

    def __init__(self, converters):
        self.converters = converters

    def run(self):
        ''' run each converter '''
        conn = get_conn()
        for converter in self.converters:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute(converter.get_sql())
            old_items = cursor.fetchall()
            for old_item in old_items:
                converter.collect_id(old_item)
                converter.collect_item(old_item)
            converter.get_manager().filter(pk__in=converter.ids).delete()
            converter.get_manager().bulk_create(converter.new_objs,
                                                batch_size=10000)


class MeetingTypeConverter(object):
    ''' grabs old meeting types and loads them into mfserver2 '''

    def __init__(self):
        self.new_objs = []
        self.ids = []

    @classmethod
    def get_sql(cls):
        ''' return the sql needed to grab old records '''
        return """select id, short_name, name, description from aabuddy_meetingtype"""

    def collect_id(self, old_item):
        ''' save old item id '''
        self.ids.append(old_item['id'])

    def collect_item(self, old_item):
        ''' turn single old db entry into corresponding new db entries '''
        self.new_objs.append(MeetingType(pk=old_item['id'],
                                         short_name=old_item['short_name'],
                                         name=old_item['name'],
                                         description=old_item['description']))

    @classmethod
    def get_manager(cls):
        ''' get the orm obj manager '''
        return MeetingType.objects


class UserConverter(MeetingTypeConverter):
    ''' converts old users to new ones '''

    @classmethod
    def get_sql(cls):
        ''' return the sql needed to grab old records '''
        return """select id, password, last_login, is_superuser, username, first_name, last_name,
                  email, is_staff, is_active, date_joined
                  from auth_user"""

    def collect_item(self, old_item):
        ''' turn single old db entry into corresponding new db entries '''
        self.new_objs.append(User(pk=old_item['id'],
                                  password=old_item['password'],
                                  last_login=old_item['last_login'],
                                  is_superuser=old_item['is_superuser'],
                                  username=old_item['username'],
                                  first_name=old_item['first_name'],
                                  last_name=old_item['last_name'],
                                  email=old_item['email'],
                                  is_staff=old_item['is_staff'],
                                  is_active=old_item['is_active'],
                                  date_joined=old_item['date_joined']))

    @classmethod
    def get_manager(cls):
        ''' get the orm obj manager '''
        return User.objects


class MeetingConverter(MeetingTypeConverter):
    ''' turn old aabuddy meetings into mfserver2 meetings '''

    @classmethod
    def get_sql(cls):
        ''' return the sql needed to grab old records '''
        return """select id, day_of_week, start_time, end_time, name, description, address,
                  ST_AsText (geo_location), creator_id, created_date
                  from aabuddy_meeting limit 15"""

    def collect_item(self, old_item):
        ''' turn single old db entry into corresponding new db entries '''
        meeting = Meeting()
        meeting.pk = old_item['id']
        meeting.day_of_week = old_item['day_of_week']
        meeting.start_time = old_item['start_time']
        meeting.end_time = old_item['end_time']
        meeting.name = old_item['name']
        meeting.description = old_item['description']
        meeting.creator_id = old_item['creator_id']
        meeting.address = old_item['address']
        meeting.created_date = old_item['created_date']
        meeting.geo_location = GEOSGeometry(old_item['st_astext'], srid=4326)
        self.new_objs.append(meeting)

    @classmethod
    def get_manager(cls):
        ''' get the orm obj manager '''
        return Meeting.objects
