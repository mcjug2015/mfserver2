# resetting password while logged out with curl



This assumes that the mfserver2 you're pointing at has been set up to send emails as specified in docs/admin_emails.md. Refer to docs/authenticated_requests.md if you don't know where to get the tokens from.



Get the tokens and post a request to the reset_password_request url with the email of the user whose password you will be resetting. This assumes meetingfinder is still using emails as usernames.
```
curl -f -k -v https://104.131.167.30/mfserver2/welcome/
curl -f -k -v -H "Content-Type: application/json" -H "X-CSRFToken: THE_TOKEN" -H "referer: https://104.131.167.30" --cookie "csrftoken=THE_COOKIE"  -X POST -d '{"email": "victor.semenov@gmail.com"}' https://104.131.167.30/mfserver2/reset_password_request/
```



The password reset link will be sent to the email address provided if they are a valid meeting finder user. They may need to dig through their spam folder. The user will need to follow the link in the email and fill out the reset password form. Once that is done the new password can be used.
