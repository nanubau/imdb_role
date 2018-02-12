from django.conf.urls import url, include

urlpatterns = [
    url(r'^v1/', include('role.v1.urls', namespace='role_v1')),

]
