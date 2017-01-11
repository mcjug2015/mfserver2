''' views module '''
# pylint: disable=no-self-use
import json
from django.contrib.auth import authenticate, login, logout
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views import View


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
