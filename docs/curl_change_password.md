# changing an authenticated user's password with curl

First we need to login and get the sessionid so as to be working with an authenticated user. If you don't know where to get the tokens/cookies from, take a look at docs/authenticated_requests.md
```
curl -f -k -v https://127.0.0.1/mfserver2/welcome/
curl -f -k -v -H "Content-Type: application/json" -H "X-CSRFToken: THE_TOKEN" -H "referer: https://127.0.0.1" --cookie "csrftoken=THE_COOKIE"  -X POST -d '{"username": "admin", "password": "admin"}' https://127.0.0.1/mfserver2/login_async/
```



Now that we have the sessionid we need to make a post request to the change_password url. Old password and new password must be supplied. If the call succeeds the user will be logged out and will need to login again with the new password.
```
curl -f -k -v --cookie "csrftoken=THE_TOKEN;sessionid=SESSIONID" -H "X-CSRFToken: THE_TOKEN" -H "referer: https://127.0.0.1"  -X POST -d '{"old_password": "admin", "new_password": "newpass123"}' https://127.0.0.1/mfserver2/change_password/
```



If the above succeeded we should be able to login with the new password and make authenticated requests.
```
curl -f -k -v -H "Content-Type: application/json" -H "X-CSRFToken: THE_TOKEN" -H "referer: https://127.0.0.1" --cookie "csrftoken=THE_COOKIE"  -X POST -d '{"username": "admin", "password": "newpass123"}' https://127.0.0.1/mfserver2/login_async/
curl -f -k -v --cookie "csrftoken=THE_TOKEN;sessionid=SESSIONID" -H "X-CSRFToken: THE_TOKEN" -H "referer: https://127.0.0.1" https://127.0.0.1/mfserver2/api/v1/auth/user/
```