from django.conf.urls import include, url
from django.http import HttpResponse
from graphene.contrib.django.views import GraphQLView

urlpatterns = [
    url(r'^frontpage/', include('djrere.frontpage.urls')),
    url(r'^$', 'djrere.frontpage.views.home')
]
