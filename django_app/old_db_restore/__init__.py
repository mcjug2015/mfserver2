''' package helps fill new db with data from old.
To do this by hand:
As reg_user do the following. Note it is up to you to get "aabuddy_mfserver2_dump.txt"
to the mfserver2 box you're working on and make sure reg_user owns it. Db password is
"mfserver2", this is not a security hole since it only accepts connections from 127.0.0.1.
If you are using an older mfserver2 you will need to pull the latest from
https://github.com/mcjug2015/mfserver2.git into /opt/mfserver2/code to get postgis_restore.pl
Not sure why you have to do the last line twice, but if you don't it doesn't work.


createdb -h127.0.0.1 -Umfserver2 old_aabuddy
psql -h127.0.0.1 -Umfserver2 old_aabuddy -c "CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;"
cd /opt/mfserver2/code/django_app/old_db_restore/
chmod 775 postgis_restore.pl
./postgis_restore.pl aabuddy_mfserver2_dump.txt | psql -h127.0.0.1 -Umfserver2 old_aabuddy
./postgis_restore.pl aabuddy_mfserver2_dump.txt | psql -h127.0.0.1 -Umfserver2 old_aabuddy
'''
