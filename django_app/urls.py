''' urls for mfserver2 django app '''
# pylint: disable=invalid-name
from tastypie.api import Api
from django.conf.urls import include, url
from django_app.views import IndexView, login_async, logout_async
from django_app.api import MeetingResource, MeetingTypeResource, UserResource


API_V1 = Api(api_name='v1')
API_V1.register(UserResource())
API_V1.register(MeetingTypeResource())
API_V1.register(MeetingResource())


urlpatterns = [
    url(r'^welcome/$', IndexView.as_view()),
    url(r'^api/', include(API_V1.urls)),
    url(r'^login_async/', login_async),
    url(r'^logout_async/', logout_async),
]
