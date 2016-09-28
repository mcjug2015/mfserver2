''' urls for mfserver2 django app '''
# pylint: disable=invalid-name
from django.conf.urls import url
from django_app.views import IndexView


urlpatterns = [
    url(r'^welcome/$', IndexView.as_view()),
]
