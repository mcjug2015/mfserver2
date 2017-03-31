''' uses old aabuddy db to safely fill mfserver2 db '''
# pylint: disable=no-member,too-few-public-methods
import psycopg2
from django_app.models import MeetingType
from django.contrib.auth.models import User


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
                converter.convert_one(old_item)


class MeetingTypeConverter(object):
    ''' grabs old meeting types and loads them into mfserver2 '''

    @classmethod
    def get_sql(cls):
        ''' return the sql needed to grab old records '''
        return """select id, short_name, name, description from aabuddy_meetingtype"""

    @classmethod
    def convert_one(cls, old_item):
        ''' turn single old db entry into corresponding new db entries '''
        MeetingType.objects.get_or_create(pk=old_item['id'],
                                          short_name=old_item['short_name'],
                                          name=old_item['name'],
                                          description=old_item['description'])


class UserConverter(object):
    ''' converts old users to new ones '''

    @classmethod
    def get_sql(cls):
        ''' return the sql needed to grab old records '''
        return """select id, password, last_login, is_superuser, username, first_name, last_name,
                  email, is_staff, is_active, date_joined
                  from auth_user"""

    @classmethod
    def convert_one(cls, old_item):
        ''' turn single old db entry into corresponding new db entries '''
        User.objects.get_or_create(pk=old_item['id'],
                                   password=old_item['password'],
                                   last_login=old_item['last_login'],
                                   is_superuser=old_item['is_superuser'],
                                   username=old_item['username'],
                                   first_name=old_item['first_name'],
                                   last_name=old_item['last_name'],
                                   email=old_item['email'],
                                   is_staff=old_item['is_staff'],
                                   is_active=old_item['is_active'],
                                   date_joined=old_item['date_joined'])
