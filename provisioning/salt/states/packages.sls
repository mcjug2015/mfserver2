postgres-repo:
  cmd.run:
    - name: yum -y install https://download.postgresql.org/pub/repos/yum/9.6/redhat/rhel-7-x86_64/pgdg-centos96-9.6-3.noarch.rpm


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
      - gcc-c++
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
      - cmd: postgres-repo


py-packages:
  pip.installed:
    - pkgs:
      - six==1.10.0
      - pyOpenSSL==16.0.0
      - virtualenv==15.0.3
    - require:
      - pkg: yum-packages
    - reload_modules: true
