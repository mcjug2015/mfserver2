venv:
  virtualenv.managed:
    - name: {{pillar['venv_folder']}}
    - user: {{pillar['regular_username']}}
    - requirements: salt://mfserver2_copy/dependencies/pip/initial.txt
    - python: /usr/bin/python3
    - require:
      - cmd: reload_firewalld
      - pkg: yum-packages
      - file: root_folder


mfserver2_precommit:
  cmd.run:
    - cwd: {{pillar['code_folder']}}
    - runas: {{pillar['regular_username']}}
    - user: {{pillar['regular_username']}}
    - name: bash -c "PATH=$PATH:{{pillar['pg_bin_path']}};source {{pillar['venv_folder']}}/bin/activate; fab precommit;"
    - require:
      - virtualenv: venv
      - cmd: postgis_extension


mfserver2:
  cmd.run:
    - cwd: {{pillar['code_folder']}}
    - runas: {{pillar['regular_username']}}
    - user: {{pillar['regular_username']}}
    - name: bash -c "PATH=$PATH:{{pillar['pg_bin_path']}};source {{pillar['venv_folder']}}/bin/activate; fab refresh_local;"
    - require:
      - cmd: mfserver2_precommit


mfserver2_sudo:
  cmd.run:
    - cwd: {{pillar['code_folder']}}
    - runas: {{pillar['sudo_username']}}
    - user: {{pillar['sudo_username']}}
    - name:
        bash -t -c "source {{pillar['venv_folder']}}/bin/activate; fab sudo_refresh_local;"
    - require:
      - cmd: mfserver2
