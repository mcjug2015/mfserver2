''' urls for mfserver2 django app '''
from django.conf.urls import url
from django_app.views import IndexView


urlpatterns = [
    url(r'^welcome/$', IndexView.as_view()),
]