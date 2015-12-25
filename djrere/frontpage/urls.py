from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from graphene.contrib.django.views import GraphQLView

from .schema import schema
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^graph-api/', csrf_exempt(GraphQLView.as_view(schema=schema))),

]
