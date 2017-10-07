postgres-repo:
  cmd.run:
    - name: yum -y install https://download.postgresql.org/pub/repos/yum/9.6/redhat/rhel-7-x86_64/pgdg-centos96-9.6-3.noarch.rpm


yum-packages:
  pkg.installed:
    - pkgs:
      - nano
      - wget
      - nginx
      - firewalld
      - setools-console
      - libcap-devel
      - net-tools
      - policycoreutils
      - uwsgi
      - uwsgi-plugin-python3
      - liberation-mono-fonts
      - liberation-narrow-fonts
      - liberation-sans-fonts
      - liberation-serif-fonts
      - {{pillar['pg_server_name']}}
      - {{pillar['pg_devel_name']}}
      - {{pillar['postgis_name']}}
    - require:
      - cmd: postgres-repo
