regular_username: reg_user
regular_user_gid: 3001
sudo_username: sudo_user
sudo_user_gid: 3002
sudo_groupname: admins
sudo_group_gid: 3003


root_folder: /opt/mfserver2
code_folder: /opt/mfserver2/code
venv_folder: /opt/mfserver2/venv
log_folder: /var/log/mfserver2
sock_folder: /var/run/mfserver2


db_name: mfserver2


# http://yum.postgresql.org/9.5/redhat/rhel-7-x86_64/
# postgresql95-server 9.5.4-1PGDG.rhel7
# postgresql95-devel 9.5.4-1PGDG.rhel7
# postgis2_95 2.2.2-1.rhel7
pg_repo: http://yum.postgresql.org/9.4/redhat/rhel-7-x86_64/
pg_server_name: postgresql94-server
pg_server_unit_name: postgresql-9.4
pg_devel_name: postgresql94-devel
postgis_name: postgis2_94
postgis_version: 2.1.8-1.rhel7
pg_setup_path: /usr/pgsql-9.4/bin/postgresql94-setup
pg_data_path: /var/lib/pgsql/9.4/data/
pg_conf_path: /var/lib/pgsql/9.4/data/postgresql.conf
pg_hba_path: /var/lib/pgsql/9.4/data/pg_hba.conf
