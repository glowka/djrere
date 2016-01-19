from django.conf import settings
from django.http import Http404
from django.template.response import TemplateResponse


def graphiql(request):
    if not settings.DEBUG:
        raise Http404()
    return TemplateResponse(request, 'graphql/graphiql.html')
