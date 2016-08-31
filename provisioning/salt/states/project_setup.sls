venv:
  virtualenv.managed:
    - name: {{pillar['venv_folder']}}
    - user: {{pillar['regular_username']}}
    - requirements: salt://mfserver2_copy/dependencies/pip/initial.txt
    - require:
      - pip: py-packages
      - file: root_folder


mfserver2:
  cmd.run:
    - cwd: {{pillar['code_folder']}}
    - runas: {{pillar['regular_username']}}
    - name: |
        bash -c "source {{pillar['venv_folder']}}/bin/activate; fab install_prod_deps;"
        bash -c "source {{pillar['venv_folder']}}/bin/activate; fab install_dev_deps;"
    - require:
      - virtualenv: venv