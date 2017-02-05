# login stuff
Read this document for how to manually make authenticated requests. There is also a helper command in django_app.management.commands.get_csrf_session.py that will take in your username and password and supply csrf token and session id. E.G. 
python manage.py get_csrf_session --initial_url https://127.0.0.1/mfserver2/welcome/ --login_url https://127.0.0.1/mfserver2/login_async/


grab the csrf token value and cookie from

curl -f -k -v https://127.0.0.1/mfserver2/welcome/


send in csrf referer + token + cookie + login creds to get session id

curl -f -k -v -H "Content-Type: application/json" -H "X-CSRFToken: THE_TOKEN" -H "referer: https://127.0.0.1" --cookie "csrftoken=THE_COOKIE"  -X POST -d '{"username": "admin", "password": "admin"}' https://127.0.0.1/mfserver2/login_async/


send in the token + session id to make authenticated requests

curl -f -k -v --cookie "csrftoken=THE_TOKEN;sessionid=dnggyjcepbv892w55ag0pyi77qwwhff4" -H "X-CSRFToken: THE_TOKEN" -H "referer: https://127.0.0.1"



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


victors-MacBook-Pro:~ vsemenov$ curl -f -k -v --cookie "csrftoken=VSbkFc6RSaAbnMrGnVySUSPqEaiSpXzQaZU4RC10O6psB7XyNiuON25KaVpIdrEZ;sessionid=2wxndvsgxnyh8rgh2liu139g6qscl3ci" -H "X-CSRFToken: VSbkFc6RSaAbnMrGnVySUSPqEaiSpXzQaZU4RC10O6psB7XyNiuON25KaVpIdrEZ" -H "referer: https://138.197.21.211" -H "Content-Type: application/json" https://138.197.21.211/mfserver2/api/v1/auth/user/1/?format=json
*   Trying 138.197.21.211...
* Connected to 138.197.21.211 (138.197.21.211) port 443 (#0)
* TLS 1.2 connection using TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
* Server certificate: localhost
> GET /mfserver2/api/v1/auth/user/1/?format=json HTTP/1.1
> Host: 138.197.21.211
> User-Agent: curl/7.43.0
> Accept: */*
> Cookie: csrftoken=VSbkFc6RSaAbnMrGnVySUSPqEaiSpXzQaZU4RC10O6psB7XyNiuON25KaVpIdrEZ;sessionid=2wxndvsgxnyh8rgh2liu139g6qscl3ci
> X-CSRFToken: VSbkFc6RSaAbnMrGnVySUSPqEaiSpXzQaZU4RC10O6psB7XyNiuON25KaVpIdrEZ
> referer: https://138.197.21.211
> Content-Type: application/json
> 
< HTTP/1.1 200 OK
< Server: nginx/1.10.2
< Date: Sat, 04 Feb 2017 17:36:24 GMT
< Content-Type: application/json
< Transfer-Encoding: chunked
< Connection: keep-alive
< Vary: Accept, Cookie
< X-Frame-Options: SAMEORIGIN
< Cache-Control: no-cache
< Strict-Transport-Security: max-age=31536000
< 
* Connection #0 to host 138.197.21.211 left intact
{"date_joined": "2017-02-04T17:23:38.078321", "email": "test@test.com", "first_name": "", "id": 1, "is_active": true, "is_staff": true, "last_login": "2017-02-04T17:30:10.312510", "last_name": "", "resource_uri": "/mfserver2/api/v1/auth/user/1/", "username": "admin"}
