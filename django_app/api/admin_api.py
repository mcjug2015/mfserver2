''' admin endpoints '''
# pylint: disable=too-few-public-methods,arguments-differ
from django.contrib.auth.models import User
from tastypie.authentication import SessionAuthentication
from tastypie.constants import ALL
from django_app.api.auth import AdminAuthorization
from django_app.api.api import ExceptionThrowingModelResource


class AdminUserResource(ExceptionThrowingModelResource):
    ''' Use this to get info about the currently logged in user. '''

    def obj_create(self, bundle, **kwargs):
        ''' create user and save password '''
        bundle = super(AdminUserResource, self).obj_create(bundle, **kwargs)
        bundle.obj.set_password(bundle.data.get('password'))
        bundle.obj.save()
        return bundle

    class Meta(object):
        ''' meta info '''
        list_allowed_methods = ['post']
        detail_allowed_methods = ['delete']
        queryset = User.objects.all()
        resource_name = 'admin_user'
        excludes = ['is_superuser']
        authentication = SessionAuthentication()
        authorization = AdminAuthorization()
        filtering = {'username': ALL}
        always_return_data = True
