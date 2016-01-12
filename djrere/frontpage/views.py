from django.conf import settings
from django.template.response import TemplateResponse


def home(request):
    return TemplateResponse(request, 'frontpage/base.html', context={'DEBUG': settings.DEBUG})
