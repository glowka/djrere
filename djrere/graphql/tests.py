from django.test import TestCase, Client
from graphql.core.utils.introspection_query import introspection_query

from .schema import schema


class SchemaTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_introspection(self):
        result = schema.execute(introspection_query)
        self.assertFalse(result.errors)
        self.assertIn('__schema', result.data)
