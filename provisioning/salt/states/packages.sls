postgres-repo:
   pkgrepo.managed:
     - name: postgres-centos
     - humanname: postgres-centos
     - baseurl: {{pillar['pg_repo']}}
     - gpgcheck: 0


yum-packages:
  pkg.installed:
    - pkgs:
      - nano
      - wget
      - nginx
      - openssl-devel
      - firewalld
      - python-devel
      - libffi-devel
      - setools-console
      - gcc
      - libcap-devel
      - net-tools
      - policycoreutils
      - uwsgi
      - uwsgi-plugin-python
      - liberation-mono-fonts
      - liberation-narrow-fonts
      - liberation-sans-fonts
      - liberation-serif-fonts
      - {{pillar['pg_server_name']}}
      - {{pillar['pg_devel_name']}}
      - {{pillar['postgis_name']}}
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
