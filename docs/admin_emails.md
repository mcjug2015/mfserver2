# Sending emails from server

Put you gmail creds into /opt/mfserver2/code/django_proj/settings.py like so:
```
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'test@gmail.com'
EMAIL_HOST_PASSWORD = 'test'
EMAIL_PORT = 587
```

Attempt and fail to send an email to yourself from the shell as reg_user
```
cd /opt/mfserver2/code/
python manage.py shell
from django.core.mail import EmailMessage
email = EmailMessage('title', 'body', to=['victor.semenov@gmail.com'])
email.send()
KABOOM
```

This will fail and you'll get an email, the email may take 5-10 minutes to arrive. click it and tell google the attempt is legit. doing the same thing after the should succeed
```
cd /opt/mfserver2/code/
python manage.py shell
from django.core.mail import EmailMessage
email = EmailMessage('title', 'body', to=['victor.semenov@gmail.com'])
email.send()
IT Works!
```

You will need to do refresh_local and sudo_refresh_local as specified in README.md. Now your mfserver2 should be able to send out registration confirmation emails and such.
