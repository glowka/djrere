from django.conf.urls import url
from graphene.contrib.django.views import GraphQLView

from .schema import schema
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^graph-api/', GraphQLView.as_view(schema=schema)),

]
