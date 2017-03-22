''' urls for mfserver2 django app '''
# pylint: disable=invalid-name
from tastypie.api import Api
from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django_app.views import (IndexView, login_async, logout_async,
                              RegisterUserView, ChangePasswordView, RequestResetPassword,
                              ResetPassword)
from django_app.api import (MeetingResource, MeetingTypeResource, UserResource,
                            SaveMeetingResource)


API_V1 = Api(api_name='v1')
API_V1.register(UserResource())
API_V1.register(MeetingTypeResource())
API_V1.register(MeetingResource())
API_V1.register(SaveMeetingResource())


urlpatterns = [
    url(r'^welcome/$', IndexView.as_view()),
    url(r'^api/', include(API_V1.urls)),
    url(r'^login_async/', login_async),
    url(r'^logout_async/', logout_async),
    url(r'^register/', RegisterUserView.as_view()),
    url(r'^reset_password_request/', RequestResetPassword.as_view()),
    url(r'^reset_password/', ResetPassword.as_view()),
    url(r'^change_password/', login_required(ChangePasswordView.as_view())),
]
