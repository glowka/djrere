import graphene
from django.utils.functional import SimpleLazyObject
from graphene import relay
from graphene.contrib.django import DjangoNode

from . import models


class Comment(DjangoNode):
    link = graphene.Field('FrontLink')
    content = graphene.String()

    class Meta:
        model = models.Comment

    def resolve_content(self, args, info):
        return self.instance.content

    def resolve_link(self, args, info):
        return self.instance.link


class FrontLink(DjangoNode):
    href = graphene.String()
    description = graphene.String()
    comments = relay.ConnectionField(Comment)

    class Meta:
        model = models.FrontLink

    def resolve_href(self, args, info):
        return self.instance.href

    def resolve_description(self, args, info):
        return self.instance.description

    def resolve_comments(self, args, info):
        return self.instance.comments.all()


class Query(graphene.ObjectType):
    front_link = relay.NodeField(FrontLink)
    comment = relay.NodeField(Comment)
    node = relay.NodeField()
    all_front_links = relay.ConnectionField(FrontLink)
    all_comments = relay.ConnectionField(Comment)

    def resolve_all_front_links(self, args, info):
        return models.FrontLink.objects.all()

    def resolve_all_comments(self, args, info):
        return models.Comment.objects.all()

local_schema = SimpleLazyObject(lambda: graphene.Schema(query=Query))
