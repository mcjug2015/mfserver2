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
      - cmd: init_postgres
