#!/bin/bash

/usr/bin/yum install -y epel-release
/usr/bin/yum install -y python2-pip
/usr/bin/pip install pip==7.1.0
/usr/bin/yum install -y salt-minion


#let salt have access to all the projects files
/usr/bin/rm -rf /tmp/mfserver2_copy/
/usr/bin/cp -R /tmp/mfserver2/ /tmp/mfserver2_copy/
/usr/bin/rm -rf /tmp/mfserver2/provisioning/salt/states/mfserver2_copy/
/usr/bin/cp -R /tmp/mfserver2_copy/ /tmp/mfserver2/provisioning/salt/states/

/usr/bin/salt-call --log-level=debug --local state.apply --file-root=/tmp/mfserver2/provisioning/salt/states/ --pillar-root=/tmp/mfserver2/provisioning/salt/pillars
