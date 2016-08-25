yum-packages:
  pkg.installed:
    - pkgs:
      - nano
      - wget
      - nginx
      - openssl-devel
      - python-devel
      - libffi-devel
      - python-pip
      - setools-console
      - gcc
      - libcap-devel
      - net-tools
      - policycoreutils
      - uwsgi
      - uwsgi-plugin-python


py-packages:
  pip.installed:
    - pkgs:
      - pyOpenSSL
      - virtualenv
    - require:
      - pkg: yum-packages

