# coding=utf-8
import graphene
from django.utils.functional import SimpleLazyObject
from graphene import relay
from graphene.contrib.django import DjangoNode
from graphql_relay import from_global_id, to_global_id
from graphql_relay.connection.arrayconnection import offset_to_cursor

from . import models
from ..utils.query import viewer_query


class Article(graphene.ObjectType):
    title = graphene.StringField()
    content = graphene.StringField()

    def resolve_title(self, args, info):
        return self._root.title

    def resolve_content(self, args, info):
        return self._root.content


class ArticleNode(relay.Node):
    title = graphene.StringField()
    content = graphene.StringField()

    def resolve_title(self, args, info):
        return self._root.title

    def resolve_content(self, args, info):
        return self._root.content

    @classmethod
    def get_node(cls, id, info=None):
        return models.Article.objects.get(pk=id)


class ArticleDjangoNode(DjangoNode):
    class Meta:
        model = models.Article
        only_fields = ['title', 'content']


class BlogQuery(graphene.ObjectType):
    """
    query {
      viewer {
        blog {
          myStr
          article(localId: 1) {
            content, title
          }
          articleNode(id: "QXJ0aWNsZU5vZGU6MQ==") {
            content, title, id
          }
          articleDjangoNode(id: "QXJ0aWNsZURqYW5nb05vZGU6MQ==") {
            content, title, id
          }
          articleDjangoNode(title: "title") {
            content, title, id
          }
        }
      }
    }

    """
    my_str = graphene.StringField()
    article = graphene.Field(Article, args={'local_id': graphene.Int().NonNull})
    articleNode = relay.NodeField(ArticleNode)
    articleDjangoNode = relay.NodeField(ArticleDjangoNode)

    def resolve_my_str(self, args, info):
        return 'my test string'

    def resolve_article(self, args, info):
        print args
        return models.Article.objects.get(pk=args.get('local_id'))


class BlogMutation(graphene.ObjectType):
    pass

local_schema = SimpleLazyObject(lambda: graphene.Schema(query=viewer_query(BlogQuery), mutation=BlogMutation))
