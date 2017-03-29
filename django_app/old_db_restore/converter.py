''' uses old aabuddy db to safely fill mfserver2 db '''
import psycopg2


def get_conn(db_host="127.0.0.1", db_port="5432", db_username="mfserver2",
             db_password="mfserver2", db_name="old_aabuddy"):
    ''' get conn for old database '''
    return psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s' port='%s'" % (db_name,
                                                                                         db_username,
                                                                                         db_host,
                                                                                         db_password,
                                                                                         db_port))
