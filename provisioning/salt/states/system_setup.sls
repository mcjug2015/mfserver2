/sbin/setenforce 0:
  cmd.run:
    - require:
      - pkg: yum-packages


/etc/sysconfig/selinux:
  file.managed:
    - source:
      - salt://mfserver2_copy/provisioning/conf/selinux/selinux_config


do_cert:
  module.run:
    - name: tls.create_self_signed_cert
    - require:
      - pkg: yum-packages
    - CN: {{pillar['ip_hostname']}}
    - ST: "MD"
    - L: "Rockville"
    - O: "MCJUG"
    - cacert_path: "/etc/nginx"
    - tls_dir: "ssl"


init_postgres:
  cmd.run:
    - name: {{pillar['pg_setup_path']}} initdb
    - unless: ls {{pillar['pg_conf_path']}}
    - require:
      - pkg: yum-packages


firewalld:
  service.running:
    - enable: True
    - require:
      - pkg: yum-packages


enable_http:
  cmd.run:
    - name: |
        firewall-cmd --zone=public --add-service=http --permanent
        firewall-cmd --zone=public --add-service=https --permanent
    - requre:
      - service: firewalld


reload_firewalld:
  cmd.run:
    - name: firewall-cmd --reload
    - requre:
      - cmd: enable_http
