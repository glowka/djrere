from django.shortcuts import render
from django.template.response import TemplateResponse


def home(request):
    return TemplateResponse(request, 'frontpage/base.html')