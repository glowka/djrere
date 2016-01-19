from django.test import TestCase, Client

from ...utils.test_cases import GraphTestMixin
from ..dummy_schema import local_schema as schema


class SchemaTests(GraphTestMixin, TestCase):
    def setUp(self):
        super(SchemaTests, self).setUp()
        self.client = Client()

    def test_page_link(self):
        query = '''
            query FetchPageLink {
                pageLink(id: "UGFnZUxpbms6MQ==") {
                    id
                }
            }
            '''
        expected = {
            'pageLink': {
                'id': 'UGFnZUxpbms6MQ=='
            }
        }

        self.assertGraphQuery(schema, query, expected)

    def test_all_page_links(self):
        query = '''
            query FetchAllPageLinks {
                allPageLinks {
                    edges {
                        node {id}
                    }
                }
            }
            '''
        expected = {
            'allPageLinks': {
                'edges': [
                    {
                        'node': {
                            'id': 'UGFnZUxpbms6MQ=='
                        }
                    }
                ]
            }
        }

        self.assertGraphQuery(schema, query, expected)
