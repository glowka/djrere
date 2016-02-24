from django.conf import settings
from django.http import Http404
from django.template.response import TemplateResponse
from graphene.contrib.django.views import GraphQLView


class UserGraphQLView(GraphQLView):
    def get_root_value(self, request):
        return {'user': request.user, 'http_request': request}


def graphiql(request):
    if not settings.DEBUG:
        raise Http404()
    return TemplateResponse(request, 'graphql/graphiql.html')
