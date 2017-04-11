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


socket_folder:
  file.directory:
    - name: {{pillar['sock_folder']}}
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


mfserver2_conf_crt:
  file.blockreplace:
    - name: {{pillar['code_folder']}}/conf/nginx/mfserver2.conf
    - marker_start: "# BEGIN SALT CRT(current one used when not provisioned by salt)"
    - marker_end: "# END SALT CRT"
    - content: "    ssl_certificate /etc/nginx/ssl/certs/{{pillar['ip_hostname']}}.crt;"
    - show_changes: True
    - append_if_not_found: False
    - require:
      - file: source_folder


mfserver2_conf_key:
  file.blockreplace:
    - name: {{pillar['code_folder']}}/conf/nginx/mfserver2.conf
    - marker_start: "# BEGIN SALT KEY(current one used when not provisioned by salt)"
    - marker_end: "# END SALT KEY"
    - content: "    ssl_certificate_key /etc/nginx/ssl/certs/{{pillar['ip_hostname']}}.key;"
    - show_changes: True
    - append_if_not_found: False
    - require:
      - file: source_folder


{% if pillar['ip_hostname'] != 'localhost' %}
settings_py_allowed_hosts:
  file.blockreplace:
    - name: {{pillar['code_folder']}}/django_proj/settings.py
    - marker_start: "# BEGIN SALT ALLOWED HOSTS(current used if not provisioned by salt)"
    - marker_end: "# END SALT ALLOWED HOSTS"
    - content: "ALLOWED_HOSTS = ['127.0.0.1', '{{pillar['ip_hostname']}}']"
    - show_changes: True
    - append_if_not_found: False
    - require:
      - file: source_folder
{% endif %}
