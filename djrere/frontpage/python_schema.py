import graphene
from django.utils.functional import SimpleLazyObject
from graphene import relay

from . import models


class Comment(relay.Node):
    link = graphene.Field('FrontLink')
    content = graphene.String()

    def resolve_content(self, args, info):
        return self._root.content

    def resolve_link(self, args, info):
        obj = self._root.link
        return FrontLink(id=obj.pk, _root=obj)

    @classmethod
    def get_node(cls, local_id, info=None):
        obj = models.Comment.objects.get(pk=local_id)
        return cls(id=obj.pk, _root=obj)


class FrontLink(relay.Node):
    href = graphene.String()
    description = graphene.String()
    comments = relay.ConnectionField(Comment)

    def resolve_href(self, args, info):
        return self._root.href

    def resolve_description(self, args, info):
        return self._root.description

    def resolve_comments(self, args, info):
        return [Comment(id=obj.pk, _root=obj) for obj in self._root.comments.all()]

    @classmethod
    def get_node(cls, local_id, info=None):
        print 'get_node'
        obj = models.FrontLink.objects.get(pk=local_id)
        return cls(id=obj.pk, _root=obj)


class Query(graphene.ObjectType):
    front_link = relay.NodeField(FrontLink)
    comment = relay.NodeField(Comment)
    node = relay.NodeField()
    all_front_links = relay.ConnectionField(FrontLink)
    all_comments = relay.ConnectionField(Comment)

    def resolve_all_front_links(self, args, info):
        return [FrontLink(id=obj.pk, _root=obj) for obj in models.FrontLink.objects.all()]

    def resolve_all_comments(self, args, info):
        return [Comment(id=obj.pk, _root=obj) for obj in models.Comment.objects.all()]

local_schema = SimpleLazyObject(lambda: graphene.Schema(query=Query))
