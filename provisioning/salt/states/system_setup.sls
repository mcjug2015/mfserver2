/sbin/setenforce 0:
  cmd.run:
    - require:
      - pip: py-packages


/etc/sysconfig/selinux:
  file.managed:
    - source:
      - salt://mfserver2_copy/provisioning/conf/selinux/selinux_config


do_cert:
  module.run:
    - name: tls.create_self_signed_cert
    - require:
      - pip: py-packages
    - CN: "localhost"
    - ST: "MD"
    - L: "Rockville"
    - O: "MCJUG"
    - cacert_path: "/etc/nginx"
    - tls_dir: "ssl"


init_postgres:
  cmd.run:
    - name: {{pillar['pg_setup_path']}} initdb
    - require:
      - pkg: yum-packages
