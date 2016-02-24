from django.test import TestCase, Client
from graphql_relay import to_global_id

from ...utils.test_cases import GraphTestMixin
from ..schema import local_schema as schema
from .. import models


class SchemaTests(GraphTestMixin, TestCase):
    def setUp(self):
        super(SchemaTests, self).setUp()
        self.client = Client()

    def create_article(self):
        return models.Article.objects.create(title='title text', content='content text')

    def test_article(self):
        article = self.create_article()
        article_gid = to_global_id('ArticleNode', article.pk)
        query = '''
            query ShowArticle {
                user {
                    articleNode(id: "%s") {
                        id,
                        title,
                        content
                    }
                }
            }
            ''' % article_gid
        expected = {
            'user': {
                "articleNode": {
                  "id": article_gid,
                  "title": article.title,
                  "content": article.content
                }
            }
        }

        self.assertGraphQuery(schema, query, expected)
