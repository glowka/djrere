from django.test import TestCase, Client

from ..dummy_schema import local_schema as schema


class SchemaTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_front_link(self):
        query = '''
            query FetchFrontLink {
                frontLink(id: "RnJvbnRMaW5rOjE=") {
                    id
                }
            }
            '''
        expected = {
            'frontLink': {
                'id': 'RnJvbnRMaW5rOjE='
            }
        }

        result = schema.execute(query)
        self.assertFalse(result.errors)
        self.assertDictEqual(result.data, expected)

    def test_all_front_links(self):
        query = '''
            query FetchAllFrontLinks {
                allFrontLinks {
                    edges {
                        node {id}
                    }
                }
            }
            '''
        expected = {
            'allFrontLinks': {
                'edges': [
                    {
                        'node': {
                            'id': 'RnJvbnRMaW5rOjE='
                        }
                    }
                ]
            }
        }

        result = schema.execute(query)
        self.assertFalse(result.errors)
        self.assertDictEqual(result.data, expected)
