'''
    fab file with commands to restore old db dump
    invoke from project root with something like:
    fab -fdjango_app/old_db_restore/fab_restore.py restore:"/opt/mfserver2/code/aabuddy_mfserver2_dump.txt"
    and
    fab -fdjango_app/old_db_restore/fab_restore.py sudo_reload_db
'''
# pylint: disable=not-context-manager
from fabric.api import local, shell_env, hide


def restore(dump_path):
    ''' create old_aabuddy db, add postgis, use postgis_restore.pl to restore '''
    with shell_env(PGPASSWORD='mfserver2'):
        local("""createdb -h127.0.0.1 -Umfserver2 old_aabuddy""")
        local('''psql -h127.0.0.1 -Umfserver2 old_aabuddy -c "CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;"''')  # noqa pylint: disable=line-too-long
        local('''chmod 775 django_app/old_db_restore/postgis_restore.pl''')
        with hide('output'):
            local('''./django_app/old_db_restore/postgis_restore.pl %s | psql -h127.0.0.1 -Umfserver2 old_aabuddy''' % dump_path)  # noqa pylint: disable=line-too-long
    local("""python manage.py fill_from_old_db""")


def sudo_reload_db():
    ''' move data from old db to new one, vacuum and reboot db '''
    local("""sudo -i -u postgres bash -c 'vacuumdb mfserver2'""")
    local("""sudo systemctl stop postgresql-9.4""")
    local("""sudo systemctl start postgresql-9.4""")
