from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # url(r'^permission/(?P<pk>\D+)',
    #  views.PermissionAPIView.as_view(), name='PermissionAPIView'),
    url(r'^genre$', views.GenreAPIView.as_view(), name='GenreAPIView'),
    url(r'^movie$', views.MovieAPIView.as_view(), name='MovieAPIView'),
    url(r'^movie-role$', views.MovieRoleAPIView.as_view(), name='MovieRoleAPIView'),
    # url(r'^role$', views.RoleAPIView.as_view(), name='RoleAPIView'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
