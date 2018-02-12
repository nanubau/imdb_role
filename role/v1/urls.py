from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # url(r'^permission/(?P<pk>\D+)',
    #  views.PermissionAPIView.as_view(), name='PermissionAPIView'),
    url(r'^permission$', views.PermissionAPIView.as_view(), name='PermissionAPIView'),
    url(r'^role-permission$', views.RolePermissionAPIView.as_view(), name='RolePermissionAPIView'),
    url(r'^role$', views.RoleAPIView.as_view(), name='RoleAPIView'),
    url(r'^user-role$', views.UserRoleAPIView.as_view(), name='UserRoleAPIView'),
    url(r'^user$', views.UserAPIView.as_view(), name='UserAPIView'),
    url(r'^login$', views.LoginAPIView.as_view(), name='LoginAPIView'),
    # url(r'^role-permission$', views.RolePermissionAPIView.as_view(), name='RolePermissionAPIView'),
    # url(r'^role$', views.RoleAPIView.as_view(), name='RoleAPIView'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
