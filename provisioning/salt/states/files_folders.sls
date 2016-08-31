root_folder:
  file.directory:
    - name: {{pillar['root_folder']}}
    - user: {{pillar['regular_username']}}
    - group: {{pillar['regular_username']}}
    - mode: 755
    - makedirs: True
    - require:
      - user: regular_user


log_folder:
  file.directory:
    - name: {{pillar['log_folder']}}
    - user: {{pillar['regular_username']}}
    - group: {{pillar['regular_username']}}
    - mode: 755
    - makedirs: True
    - require:
      - user: regular_user


source_folder:
  file.recurse:
    - name: {{pillar['code_folder']}}
    - user: {{pillar['regular_username']}}
    - group: {{pillar['regular_username']}}
    - dir_mode: 2755
    - file_mode: '0644'
    - source: salt://mfserver2_copy
    - include_empty: True
    - require:
      - file: root_folder
