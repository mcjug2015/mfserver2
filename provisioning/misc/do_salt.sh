#!/bin/bash

/usr/bin/curl -o /tmp/epel-release.rpm http://mirror.sfo12.us.leaseweb.net/epel/7/x86_64/e/epel-release-7-8.noarch.rpm
/usr/bin/rpm -Uvh /tmp/epel-release.rpm
/usr/bin/yum install -y systemd-libs-219-19.el7_2.11.x86_64 systemd-python-219-19.el7_2.11.x86_64 systemd-219-19.el7_2.11.x86_64
/usr/bin/yum install -y salt-minion

#let salt have access to all the projects files
/usr/bin/rm -rf /tmp/mfserver2_copy/
/usr/bin/cp -R /tmp/mfserver2/ /tmp/mfserver2_copy/
/usr/bin/rm -rf /tmp/mfserver2/provisioning/salt/states/mfserver2_copy/
/usr/bin/cp -R /tmp/mfserver2_copy/ /tmp/mfserver2/provisioning/salt/states/

/usr/bin/salt-call --log-level=debug --local state.apply --file-root=/tmp/mfserver2/provisioning/salt/states/ --pillar-root=/tmp/mfserver2/provisioning/salt/pillars
