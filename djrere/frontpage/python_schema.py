import graphene
from django.utils.functional import SimpleLazyObject
from graphene import relay

from . import models


class PageComment(relay.Node):
    link = graphene.Field('PageLink')
    content = graphene.String()

    def resolve_content(self, args, info):
        return self._root.content

    def resolve_link(self, args, info):
        obj = self._root.link
        return PageLink(id=obj.pk, _root=obj)

    @classmethod
    def get_node(cls, local_id, info=None):
        obj = models.PageComment.objects.get(pk=local_id)
        return cls(id=obj.pk, _root=obj)


class PageLink(relay.Node):
    href = graphene.String()
    description = graphene.String()
    page_comments = relay.ConnectionField(PageComment)

    def resolve_href(self, args, info):
        return self._root.href

    def resolve_description(self, args, info):
        return self._root.description

    def resolve_page_comments(self, args, info):
        return [PageComment(id=obj.pk, _root=obj) for obj in self._root.page_comments.all()]

    @classmethod
    def get_node(cls, local_id, info=None):
        print 'get_node'
        obj = models.PageLink.objects.get(pk=local_id)
        return cls(id=obj.pk, _root=obj)


class Query(graphene.ObjectType):
    page_link = relay.NodeField(PageLink)
    page_comment = relay.NodeField(PageComment)
    node = relay.NodeField()
    all_page_links = relay.ConnectionField(PageLink)
    all_page_comments = relay.ConnectionField(PageComment)

    def resolve_all_page_links(self, args, info):
        return [PageLink(id=obj.pk, _root=obj) for obj in models.PageLink.objects.all()]

    def resolve_all_page_comments(self, args, info):
        return [PageComment(id=obj.pk, _root=obj) for obj in models.PageComment.objects.all()]

local_schema = SimpleLazyObject(lambda: graphene.Schema(query=Query))
