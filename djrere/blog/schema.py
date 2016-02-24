# coding=utf-8
import graphene
from django.utils.functional import SimpleLazyObject
from graphene import relay
from graphene.contrib.django import DjangoNode
from graphql_relay import from_global_id, to_global_id
from graphql_relay.connection.arrayconnection import offset_to_cursor

from . import models
from ..utils.query import user_wrapped_query


class DjangoConnection(relay.Connection):
    total_count = graphene.Int()

    def resolve_total_count(self, args, info):
        return self._connection_data.count()


class Article(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()

    def resolve_title(self, args, info):
        return self._root.title

    def resolve_content(self, args, info):
        return self._root.content


class ArticleNode(relay.Node):
    title = graphene.String()
    content = graphene.String()

    connection_type = DjangoConnection

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


class Blog(relay.Node):
    my_str = graphene.StringField()
    article = graphene.Field(Article, args={'local_id': graphene.Int().NonNull})
    article2 = graphene.Field(Article, args={'local_id': graphene.Int().NonNull},
                              resolver=lambda self, args, info: models.Article.objects.get(pk=args.get('local_id')))
    article_node = relay.NodeField(ArticleNode)
    article_django_node = relay.NodeField(ArticleDjangoNode)

    articles = relay.ConnectionField(ArticleNode)

    def resolve_my_str(self, args, info):
        return 'my test string'

    def resolve_article(self, args, info):
        return models.Article.objects.get(pk=args.get('local_id'))

    def resolve_articles(self, args, info):
        return models.Article.objects.filter()

    @classmethod
    def get_node(cls, id):
        return cls(id=id)


class BlogMutation(graphene.ObjectType):
    pass

local_schema = SimpleLazyObject(lambda: graphene.Schema(query=user_wrapped_query(Blog)))
