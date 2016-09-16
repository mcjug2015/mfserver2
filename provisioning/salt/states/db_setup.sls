pg_conf:
  file.blockreplace:
    - name: {{pillar['pg_conf_path']}}
    - marker_start: "# BLOCK TOP : salt managed zone : postgresql.conf : please do not edit"
    - marker_end: "# BLOCK BOTTOM : end of salt managed zone --"
    - content: |
        data_directory = '/var/lib/pgsql/9.4/data'
        listen_addresses = '*'
        port = 5432
    - show_changes: True
    - append_if_not_found: True
    - require:
      - cmd: init_postgres


{{pillar['pg_hba_path']}}:
  file.managed:
    - source:
      - salt://mfserver2_copy/conf/psql/pg_hba.conf
    - require:
      - file: pg_conf


{{pillar['pg_server_unit_name']}}:
  service.running:
    - enable: True
    - require:
      - file: {{pillar['pg_hba_path']}}


mfserver2_db_user:
  postgres_user.present:
    - name: {{pillar['db_name']}}
    - password: {{pillar['db_name']}}
    - user: postgres
    - require:
      - service: {{pillar['pg_server_unit_name']}}


mfserver2_db:
  postgres_database.present:
    - name: {{pillar['db_name']}}
    - user: postgres
    - require:
      - postgres_user: mfserver2_db_user


postgis_extension:
  cmd.run:
    - name: /usr/bin/psql {{pillar['db_name']}} -c "CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;"
    - runas: postgres
    - user: postgres
    - require:
      - postgres_database: mfserver2_db
