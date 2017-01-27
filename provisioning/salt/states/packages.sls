postgres-repo:
   pkgrepo.managed:
     - name: postgres-centos
     - humanname: postgres-centos
     - baseurl: {{pillar['pg_repo']}}
     - gpgcheck: 0


yum-packages:
  pkg.installed:
    - pkgs:
      - nano: 2.3.1-10.el7
      - wget
      - nginx
      - openssl-devel
      - python-devel: 2.7.5-48.el7
      - libffi-devel: 3.0.13-18.el7
      - setools-console: 3.3.8-1.1.el7
      - gcc: 4.8.5-11.el7
      - libcap-devel: 2.22-8.el7
      - net-tools: 2.0-0.17.20131004git.el7
      - policycoreutils: 2.5-9.el7
      - uwsgi: 2.0.14-3.el7
      - uwsgi-plugin-python: 2.0.14-3.el7
      - liberation-mono-fonts
      - liberation-narrow-fonts
      - liberation-sans-fonts
      - liberation-serif-fonts
      - {{pillar['pg_server_name']}}: {{pillar['pg_server_version']}}
      - {{pillar['pg_devel_name']}}: {{pillar['pg_devel_version']}}
      - {{pillar['postgis_name']}}: {{pillar['postgis_version']}}
    - require:
      - pkgrepo: postgres-repo


py-packages:
  pip.installed:
    - pkgs:
      - six==1.10.0
      - pyOpenSSL==16.0.0
      - virtualenv==15.0.3
    - require:
      - pkg: yum-packages
