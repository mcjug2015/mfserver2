''' package helps fill new db with data from old.
createdb -h127.0.0.1 -Umfserver2 old_aabuddy
psql -h127.0.0.1 -Umfserver2 old_aabuddy -c "CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;"
./postgis_restore.pl ~/git/mfserver2/dump20170325.txt | psql -h127.0.0.1 -Umfserver2 old_aabuddy
'''
