from django.test import TestCase, Client
from graphql_relay import to_global_id

from ..schema import local_schema as schema
from .. import models


class SchemaTests(TestCase):
    def setUp(self):
        self.client = Client()

    def create_front_link(self):
        return models.FrontLink.objects.create(href='www.example.com', description='description text')

    def create_comment(self, link):
        return models.Comment.objects.create(link=link, content='content text')

    def test_front_link(self):
        link = self.create_front_link()
        link_gid = to_global_id(link.__class__.__name__, link.pk)
        query = '''
            query FetchFrontLink {
                viewer {
                    frontLink(id: "%s") {
                        id
                    }
                }
            }
            ''' % link_gid
        expected = {
            'viewer': {
                'frontLink': {
                    'id': link_gid
                }
            }
        }

        result = schema.execute(query)
        self.assertFalse(result.errors)
        self.assertDictEqual(result.data, expected)

    def test_all_front_links(self):
        link = self.create_front_link()
        link_gid = to_global_id(link.__class__.__name__, link.pk)

        query = '''
            query FetchAllFrontLinks {
                viewer {
                    allFrontLinks {
                        edges {
                            node {id}
                        }
                    }
                }
            }
            '''
        expected = {
            'viewer': {
                'allFrontLinks': {
                    'edges': [
                        {
                            'node': {
                                'id': link_gid
                            }
                        }
                    ]
                }
            }
        }

        result = schema.execute(query)
        self.assertFalse(result.errors)
        self.assertDictEqual(result.data, expected)
