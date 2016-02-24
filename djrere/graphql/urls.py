from django.conf.urls import url
from graphene.contrib.django.views import GraphQLView

from . import views
from .schema import schema

urlpatterns = [
    url(r'^api/', views.UserGraphQLView.as_view(schema=schema), name='api'),
    url(r'^graphiql/', views.graphiql, name='graphiql')
]
