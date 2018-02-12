from django.conf.urls import url, include

urlpatterns = [
    url(r'^v1/', include('movies.v1.urls', namespace='movies_v1')),

]
