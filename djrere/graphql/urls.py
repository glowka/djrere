from django.conf.urls import url
from graphene.contrib.django.views import GraphQLView

from .schema import schema

urlpatterns = [
    url(r'^api/', GraphQLView.as_view(schema=schema)),

]
