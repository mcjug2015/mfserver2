# mfserver2
meeting finder server version 2


To setup locally do:

sudo yum install -y git
git clone https://github.com/mcjug2015/mfserver2.git /tmp/mfserver2
sh /tmp/mfserver2/provisioning/misc/do_salt.sh

If ip address is different from 127.0.0.1 go to django_proj/settings.py and add ip to ALLOWED_HOSTS


To make csrf and sessionid authenticated requests take a look in docs.authenticated_requests.md or django_app.management.commands.get_csrf_session.py


One you have a csrf and session id you can save meetings for the user you logged in with:

-H "Content-Type: application/json" -X POST -d'{"geo_location": {"coordinates": [-77.0, 39.0], "type": "Point"}, "name": "posted meeting", "creator": "/mfserver2/api/v1/auth/user/1/", "day_of_week": 7, "start_time": "22:30+03:00", "end_time": "23:30+03:00", "description": "posted meeting", "address": "another address", "is_active": true, "types": []}' https://127.0.0.1/mfserver2/api/v1/savemeeting/?format=json

