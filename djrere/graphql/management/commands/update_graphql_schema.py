# -*- coding: utf-8 -*-
import json
import os

from django.core.management.base import BaseCommand
from graphql.core.utils.introspection_query import introspection_query

from djrere.graphql.schema import schema


class Command(BaseCommand):
    help = ''
    args = ''
    can_import_settings = True

    def handle(self, *args, **options):
        from django.conf import settings

        json_schema = json.dumps({'data': schema.execute(introspection_query).data})
        filepath = os.path.join(getattr(settings, 'BASE_PATH', './'), 'var/graphql/schema.json')
        with open(filepath, mode='wb') as f:
            f.write(json_schema)
