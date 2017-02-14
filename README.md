# mfserver2
meeting finder server version 2


To setup locally get a centos7 that you can ssh to without port forwarding and as root do:
```
yum install -y git
git clone https://github.com/mcjug2015/mfserver2.git /tmp/mfserver2
sh /tmp/mfserver2/provisioning/misc/do_salt.sh
```

If ip address is different from 127.0.0.1 switch to reg_user and go to /opt/mfserver2/code/django_proj/settings.py and add ip to ALLOWED_HOSTS at line 28(it'll look something like this ALLOWED_HOSTS = ['127.0.0.1', '192.168.2.5']). After that do:
```
su - reg_user
cd /opt/mfserver2/code
source /opt/mfserver2/venv/bin/activate
fab refresh_local
```
and finally:
```
su - sudo_user
cd /opt/mfserver2/code
source /opt/mfserver2/venv/bin/activate
fab sudo_refresh_local
```
Now go to https://ip_address/admin/ or https://ip_address/mfserver2/welcome/ and stuff should come up. U/p is admin/admin


To make csrf and sessionid authenticated requests take a look in docs.authenticated_requests.md or django_app.management.commands.get_csrf_session.py


One you have a csrf and session id you can save meetings for the user you logged in with:
```
-H "Content-Type: application/json" -X POST -d'{"geo_location": {"coordinates": [-77.0, 39.0], "type": "Point"}, "name": "posted meeting", "creator": "/mfserver2/api/v1/auth/user/1/", "day_of_week": 7, "start_time": "22:30+03:00", "end_time": "23:30+03:00", "description": "posted meeting", "address": "another address", "is_active": true, "types": []}' https://127.0.0.1/mfserver2/api/v1/savemeeting/?format=json
```

