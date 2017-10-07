''' views module '''
# pylint: disable=no-self-use, no-member
import json
import logging
from django.contrib.auth import authenticate, login, logout
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django_app.services import user_service
LOGGER = logging.getLogger(__name__)


def login_async(request):
    ''' get username and password from json request body, log user in '''
    json_in = json.loads(request.body.decode('utf-8'))
    username = json_in['username']
    password = json_in['password']
    user = authenticate(username=username, password=password)
    if user is not None:  # pylint:disable=no-else-return
        login(request, user)
        return JsonResponse(status=200, data={'status': 'good to go',
                                              'status_code': 200})
    else:
        return JsonResponse(status=403, data={'status': 'wrong u/p or inactive user',
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
        json_obj = json.loads(request.body.decode('utf-8'))
        email = json_obj["email"]
        password = json_obj["password"]
        result = user_service.create_user_and_conf(email, password)
        if result["user"]:
            LOGGER.info("Registered user %s, status: %s", email, result["status"])
            link_address = request.build_absolute_uri() + '?confirmation=' + result["conf"].confirmation_key
            message_text = "Click the link below to complete the registration process\n%s" % link_address
            user_service.send_email_to_user(result["user"],
                                            "Thank you for registering on Meeting Finder",
                                            message_text)
            return HttpResponse(status=201,
                                content="User %s registered, awaiting confirmation" % email)
        LOGGER.error("Failed to register user %s, reason: %s", email, result["status"])
        return HttpResponse(status=400,
                            content="User %s exists and can not re-register" % email)


class ChangePasswordView(View):
    ''' view for changing password '''

    def post(self, request):
        ''' parse old and new password from request, change user password, sign him out '''
        json_obj = json.loads(request.body.decode('utf-8'))
        old_password = json_obj["old_password"]
        new_password = json_obj["new_password"]
        if not request.user.check_password(old_password):
            return HttpResponse(status=401,
                                content="Incorrect old password")
        request.user.set_password(new_password)
        request.user.save()
        logout(request)
        content = "Successfully changed password. You will need to log in with the new one."
        return HttpResponse(status=200,
                            content=content)


class RequestResetPassword(View):
    ''' view to reset password '''

    def get(self, request):
        ''' show user the form to reset password '''
        conf_key = request.GET.get('confirmation', None)
        conf, response = user_service.get_conf_and_response(conf_key, "password_reset")
        if response:
            response.content = "Invalid password reset link"
            return response
        return render(request, 'user/reset_password.html',
                      context={"reset_conf": conf})

    def post(self, request):
        ''' generate reset conf for user and send email with reset link '''
        json_obj = json.loads(request.body.decode('utf-8'))
        email = json_obj["email"]
        result = user_service.request_password_reset(email)
        if result["conf"]:
            LOGGER.info("Sending reset password link to user %s", email)
            link_address = request.build_absolute_uri() + '?confirmation=' + result["conf"].confirmation_key
            message_text = "Click the link below to reset your meetingfinder password\n%s" % link_address
            user_service.send_email_to_user(result["user"],
                                            "Your meeting finder password reset",
                                            message_text)
            return HttpResponse(status=200,
                                content="Emailed password reset link to user %s " % email)
        LOGGER.error("Failed reset password for user %s, reason: %s", email, result["status"])
        return HttpResponse(status=400, content=result["status"])


class ResetPassword(View):
    ''' view for resetting the password with user conf '''

    def post(self, request):
        '''
            if password and retype password match, reset it,
            else return page with validation error
        '''
        conf_key = request.POST.get("reset_conf", None)
        conf, response = user_service.get_conf_and_response(conf_key, "password_reset")
        if response:
            response.content = "Invalid password reset link"
            return response
        errors_list = []
        password = request.POST.get("password", None)
        retype_password = request.POST.get("retype_password", None)
        if password != retype_password:
            errors_list.append("Passwords did not match")
        if len(password) < 6:
            errors_list.append("Password must be longer than 6 characters")
        if errors_list:
            return render(request, 'user/reset_password.html',
                          context={"errors_list": errors_list,
                                   "reset_conf": conf})
        result = user_service.reset_password(conf, password)
        if "Successfully" in result:
            status = 200
        else:
            status = 400
        return HttpResponse(status=status, content=result)
