from django.conf.urls import include, url
from django.http import HttpResponse

urlpatterns = [
    url(r'^graph-api/', lambda request: HttpResponse()),
    url(r'^frontpage/', include('djrere.frontpage.urls')),
    url(r'^$', 'djrere.frontpage.views.home')
]
