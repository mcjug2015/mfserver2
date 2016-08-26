yum-packages:
  pkg.installed:
    - pkgs:
      - nano: 2.3.1-10.el7
      - wget: 1.14-10.el7_0.1
      - nginx
      - openssl-devel
      - python-devel: 2.7.5-38.el7_2
      - libffi-devel: 3.0.13-16.el7
      - python-pip: 7.1.0-1.el7
      - setools-console: 3.3.7-46.el7
      - gcc: 4.8.5-4.el7
      - libcap-devel: 2.22-8.el7
      - net-tools: 2.0-0.17.20131004git.el7
      - policycoreutils: 2.2.5-20.el7
      - uwsgi: 2.0.13.1-2.el7
      - uwsgi-plugin-python: 2.0.13.1-2.el7


py-packages:
  pip.installed:
    - pkgs:
      - pyOpenSSL==16.0.0
      - virtualenv==15.0.3
    - require:
      - pkg: yum-packages

