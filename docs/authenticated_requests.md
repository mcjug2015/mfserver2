# login stuff
Read this document for how to manually make authenticated requests. There is also a helper command in django_app.management.commands.get_csrf_session.py that will take in your username and password and supply csrf token and session id


grab the csrf token value and cookie from
curl -f -k -v http://127.0.0.1:8000/mfserver2/welcome/

send in csrf token + cookie + login creds to get session id
curl -f -k -v -H "Content-Type: application/json" -H "X-CSRFToken: THE_TOKEN" --cookie "csrftoken=THE_COOKIE"  -X POST -d '{"username": "admin", "password": "admin"}' http://127.0.0.1:8000/mfserver2/login_async/

send in the latest csrf cookie and session id to make authenticated requests
curl -f -k -v --cookie "csrftoken=THE_LATEST_CSRF" --cookie "sessionid=THE_SESSIONID" http://127.0.0.1:8000/mfserver2/api/v1/auth/user/1/?format=json


## login stuff details
[dtuser@localhost code]$ curl -f -k -v http://127.0.0.1:8000/mfserver2/welcome/
* About to connect() to 127.0.0.1 port 8000 (#0)
*   Trying 127.0.0.1...
* Connected to 127.0.0.1 (127.0.0.1) port 8000 (#0)
> GET /mfserver2/welcome/ HTTP/1.1
> User-Agent: curl/7.29.0
> Host: 127.0.0.1:8000
> Accept: */*
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Date: Fri, 13 Jan 2017 01:29:24 GMT
< Server: WSGIServer/0.1 Python/2.7.5
< Vary: Cookie
< X-Frame-Options: SAMEORIGIN
< Content-Type: text/html; charset=utf-8
< Set-Cookie:  csrftoken=THE_COOKIE; expires=Fri, 12-Jan-2018 01:29:24 GMT; Max-Age=31449600; Path=/
< 
<html>
<head>
    <title>MFServer2</title>
</head>
<body>
    <input type='hidden' name='csrfmiddlewaretoken' value='THE_TOKEN' />
    <div>Welcome to meeting finder server 2</div>
    <div>curl/7.29.0</div>
</body>
* Closing connection 0


[dtuser@localhost code]$ curl -f -k -v -H "Content-Type: application/json" -H "X-CSRFToken: Ss9C9wEUJ1lgbCJfkPTSOtprmv87xT36ZssFc4OZw8jrPswtacGvA38MxcuuNcx8" --cookie "csrftoken=w5AtKa57z6ZTW1BhhJ1o3zmzsRyOBAUlD5TwNIfcmdX4ARov76O1P95UDyUbRTon"  -X POST -d '{"username": "admin", "password": "admin"}' http://127.0.0.1:8000/mfserver2/login_async/
* About to connect() to 127.0.0.1 port 8000 (#0)
*   Trying 127.0.0.1...
* Connected to 127.0.0.1 (127.0.0.1) port 8000 (#0)
> POST /mfserver2/login_async/ HTTP/1.1
> User-Agent: curl/7.29.0
> Host: 127.0.0.1:8000
> Accept: */*
> Cookie: csrftoken=w5AtKa57z6ZTW1BhhJ1o3zmzsRyOBAUlD5TwNIfcmdX4ARov76O1P95UDyUbRTon
> Content-Type: application/json
> X-CSRFToken: Ss9C9wEUJ1lgbCJfkPTSOtprmv87xT36ZssFc4OZw8jrPswtacGvA38MxcuuNcx8
> Content-Length: 42
> 
* upload completely sent off: 42 out of 42 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Date: Fri, 13 Jan 2017 01:32:33 GMT
< Server: WSGIServer/0.1 Python/2.7.5
< Vary: Cookie
< X-Frame-Options: SAMEORIGIN
< Content-Type: application/json
< Set-Cookie:  csrftoken=GU9P5ta5EKp3AV1aIggYIDdKirchsJrnu3tzfRVXtY2JWhMGw1OiBpPDV3nDlxCW; expires=Fri, 12-Jan-2018 01:32:33 GMT; Max-Age=31449600; Path=/
< Set-Cookie:  sessionid=THE_SESSIONID; expires=Fri, 27-Jan-2017 01:32:33 GMT; httponly; Max-Age=1209600; Path=/
< 
* Closing connection 0
{"status": "good to go", "status_code": 200}


[dtuser@localhost code]$ curl -f -k -v --cookie "csrftoken=GU9P5ta5EKp3AV1aIggYIDdKirchsJrnu3tzfRVXtY2JWhMGw1OiBpPDV3nDlxCW" --cookie "sessionid=ax19nlkys9069gi3rtslv1h9wjnk0o7e" http://127.0.0.1:8000/mfserver2/api/v1/auth/user/1/?format=json
* About to connect() to 127.0.0.1 port 8000 (#0)
*   Trying 127.0.0.1...
* Connected to 127.0.0.1 (127.0.0.1) port 8000 (#0)
> GET /mfserver2/api/v1/auth/user/1/?format=json HTTP/1.1
> User-Agent: curl/7.29.0
> Host: 127.0.0.1:8000
> Accept: */*
> Cookie: sessionid=ax19nlkys9069gi3rtslv1h9wjnk0o7e
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Date: Fri, 13 Jan 2017 01:44:03 GMT
< Server: WSGIServer/0.1 Python/2.7.5
< Vary: Accept, Cookie
< X-Frame-Options: SAMEORIGIN
< Content-Type: application/json
< Cache-Control: no-cache
< 
* Closing connection 0
{"date_joined": "2016-09-21T00:37:55.385925", "email": "test@test.com", "first_name": "", "id": 1, "is_active": true, "is_staff": true, "last_login": "2017-01-13T01:32:33.570347", "last_name": "", "resource_uri": "/mfserver2/api/v1/auth/user/1/", "username": "admin"}