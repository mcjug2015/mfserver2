''' views module '''
# pylint: disable=no-self-use
import json
import logging
import django.core.mail as django_mail
from django.contrib.auth import authenticate, login, logout
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django_app.services import user_service
LOGGER = logging.getLogger(__name__)


def login_async(request):
    ''' get username and password from json request body, log user in '''
    json_in = json.loads(request.body)
    username = json_in['username']
    password = json_in['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'status': 'good to go',
                             'status_code': 200})
    else:
        return JsonResponse({'status': 'wrong u/p or inactive user',
                             'status_code': 403})


def logout_async(request):
    ''' logout the user associated with the request, no check if currently logged in. '''
    logout(request)
    return JsonResponse({'status': 'logout success'})


class IndexView(View):
    ''' Class for the main page '''

    def get(self, request):
        ''' get handler '''
        return render(request, 'index.html')


class RegisterUserView(View):
    ''' view for user registration '''

    def get(self, request):
        ''' use the conf to activate the user '''
        conf_key = request.GET.get('confirmation', None)
        result = user_service.complete_user_registration(conf_key)
        return HttpResponse(status=result["code"],
                            content=result["status"])

    def post(self, request):
        ''' register user with details provided '''
        json_obj = json.loads(request.body)
        email = json_obj["email"]
        password = json_obj["password"]
        result = user_service.create_user_and_conf(email, email, password)
        if result["user"]:
            LOGGER.info("Registered user %s, status: %s", email, result["status"])
            link_address = request.build_absolute_uri() + '/?confirmation=' + result["conf"].confirmation_key
            message_text = "Click the link below to complete the registration process\n%s" % link_address
            send_email_to_user(result["user"], "Thank you for registering on Meeting Finder", message_text)
            return HttpResponse(status=201,
                                content="User %s registered, awaiting confirmation" % email)
        LOGGER.error("Failed to register user %s, reason: %s", email, result["status"])
        return HttpResponse(status=400,
                            content="User %s exists and can not re-register" % email)


def send_email_to_user(user, subject_text, message_text):
    ''' send email to user with supplied subject and body '''
    LOGGER.debug("About to send conf email with message %s", message_text)
    django_mail.send_mail(subject=subject_text, message=message_text,
                          from_email="meetingfinder@noreply.com",
                          recipient_list=[user.email], fail_silently=False)
