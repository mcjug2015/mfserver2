#!/bin/bash

/usr/bin/yum install -y epel-release
/usr/bin/yum install -y gcc gcc-c++ libffi-devel python-devel openssl-devel
/usr/bin/yum install -y python2-pip
/usr/bin/pip install six
/usr/bin/pip install pyOpenSSL
/usr/bin/yum install -y salt-minion


/usr/bin/yum install -y python34-devel python34 python34-pip
/usr/bin/pip3 install paramiko
/usr/bin/pip3 install virtualenv


#let salt have access to all the projects files
/usr/bin/rm -rf /tmp/mfserver2_copy/
/usr/bin/cp -R /tmp/mfserver2/ /tmp/mfserver2_copy/
/usr/bin/rm -rf /tmp/mfserver2/provisioning/salt/states/mfserver2_copy/
/usr/bin/cp -R /tmp/mfserver2_copy/ /tmp/mfserver2/provisioning/salt/states/

/usr/bin/salt-call --log-level=debug --local state.apply --file-root=/tmp/mfserver2/provisioning/salt/states/ --pillar-root=/tmp/mfserver2/provisioning/salt/pillars
