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


{% set the_ip = 'localhost' %}
{% if 'ip_interfaces' in grains and 'eth0' in grains['ip_interfaces'] and grains['ip_interfaces']['eth0'] and grains['ip_interfaces']['eth0'][0] %}
    {% set the_ip = grains['ip_interfaces']['eth0'][0] %}
{% endif %}
ip_hostname: {{the_ip}}


db_name: mfserver2


# http://yum.postgresql.org/9.5/redhat/rhel-7-x86_64/
# postgresql95-server 9.5.4-1PGDG.rhel7
# postgresql95-devel 9.5.4-1PGDG.rhel7
# postgis2_95 2.2.2-1.rhel7
pg_repo: https://yum.postgresql.org/9.6/redhat/rhel-7-x86_64/
pg_server_name: postgresql96-server
pg_server_unit_name: postgresql-9.6
pg_devel_name: postgresql96-devel
postgis_name: postgis2_96
postgis_version: 2.1.8-1.rhel7
pg_setup_path: /usr/pgsql-9.6/bin/postgresql96-setup
pg_data_path: /var/lib/pgsql/9.6/data/
pg_conf_path: /var/lib/pgsql/9.6/data/postgresql.conf
pg_hba_path: /var/lib/pgsql/9.6/data/pg_hba.conf
pg_bin_path: /usr/pgsql-9.6/bin/
