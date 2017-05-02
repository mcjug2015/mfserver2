# submitting meetingnotthere for a meeting
First you will need to procure a resource_uri for the meeting that you want to mark not there. It will look kind of like this "/mfserver2/api/v1/meeting/1/". Once you have that you can send a meetingnotthere for that meeting. You can pass in the session_id of a logged in user to associate the meetingnotthere with that user, or you can submit an anonymous meetingnotthere. If you don't know where to get the tokens/cookies from, take a look at docs/authenticated_requests.md
```
curl -f -k -v -H "Content-Type: application/json" --cookie "csrftoken=THE_TOKEN;sessionid=THE_SESSION" -H "X-CSRFToken: THE_TOKEN" -H "referer: https://107.170.53.103" -X POST -d '{"meeting": "THE_RESOURCE_URI", "unique_phone_id": "abc", "note": "123"}' https://107.170.53.103/mfserver2/api/v1/meetingnotthere/
```


or without the sessionid
```
curl -f -k -v -H "Content-Type: application/json" -H "referer: https://107.170.53.103" -X POST -d '{"meeting": "/mfserver2/api/v1/meeting/1/", "unique_phone_id": "abcZZZ", "note": "123ZZZ"}' https://107.170.53.103/mfserver2/api/v1/meetingnotthere/
```


There isn't much you can do after submitting a meetingnotthere. The process is - they get submitted, I see them on the server and inactivate the meeting they are for if they look legitimate.
