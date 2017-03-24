# registering users with curl

This assumes that the mfserver2 you're pointing at has been set up to send emails as specified in docs/admin_emails.md. Refer to docs/authenticated_requests.md if you don't know where to get the tokens from.
```
curl -f -k -v https://159.203.91.166/mfserver2/welcome/
curl -f -k -v -H "Content-Type: application/json" -H "X-CSRFToken: THE_TOKEN" -H "referer: https://159.203.91.166" --cookie "csrftoken=THE_COOKIE"  -X POST -d '{"email": "test@test.com", "password": "fake_password"}' https://159.203.91.166/mfserver2/register/
```

At this point you will need to go to the email address you're registering and click the link that was provided in it. This will complete the user registration process and enable that user to login and post meetings.



First you need to login and grab the session_id by logging in
```
curl -f -k -v -H "Content-Type: application/json" -H "X-CSRFToken: THE_TOKEN" -H "referer: https://159.203.91.166" --cookie "csrftoken=THE_COOKIE"  -X POST -d '{"username": "test@test.com", "password": "fake_password"}' https://159.203.91.166/mfserver2/login_async/
```



Next step is to rerieve the logged in user resource_uri
```
curl -f -k -v --cookie "csrftoken=THE_TOKEN;sessionid=SESSION_ID" -H "X-CSRFToken: THE_TOKEN" -H "referer: https://159.203.91.166" https://159.203.91.166/mfserver2/api/v1/auth/user/
```
This will return data about the logged in user including something like "resource_uri": "/mfserver2/api/v1/auth/user/2/"



Now that we have the resource uri of the logged in user and his token and session id we can submit meetings on his behalf. Notice the "creator" field is equal to the resource uri we got in the previous step
```
curl -f -k -v --cookie "csrftoken=THE_TOKEN;sessionid=SESSION_ID" -H "X-CSRFToken: THE_TOKEN" -H "referer: https://159.203.91.166" -H "Content-Type: application/json" -X POST -d'{"geo_location": {"coordinates": [-77.0, 39.0], "type": "Point"}, "name": "posted meeting", "creator": "/mfserver2/api/v1/auth/user/2/", "day_of_week": 7, "start_time": "22:30", "end_time": "23:30", "description": "posted meeting", "address": "another address", "is_active": true, "types": []}' https://159.203.91.166/mfserver2/api/v1/savemeeting/?format=json
```
