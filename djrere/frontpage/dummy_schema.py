import graphene
from django.utils.functional import SimpleLazyObject
from graphene import relay
from graphql_relay import from_global_id


def get_node(global_id):
    node_class, local_id = from_global_id(global_id)
    node_class(id=global_id)


class AwareNode(relay.Node):
    class Meta:
        abstract = True

    @classmethod
    def get_node(cls, local_id=1, info=None):
        return cls(id=local_id)


class PageComment(AwareNode):
    link = graphene.Field('PageLink')
    content = graphene.String()

    def resolve_content(self, args, info):
        return getattr(self, 'content', 'content_value')

    def resolve_link(self, args, info):
        return getattr(self, 'link', PageLink.get_node())


class PageLink(AwareNode):
    href = graphene.String()
    description = graphene.String()
    page_comments = relay.ConnectionField(PageComment)

    def resolve_href(self, args, info):
        return getattr(self, 'href', 'href_value')

    def resolve_description(self, args, info):
        return getattr(self, 'desc', 'desc_value')

    def resolve_page_comments(self, args, info):
        return [PageComment.get_node()]


class Query(graphene.ObjectType):
    page_link = relay.NodeField(PageLink)
    page_comment = relay.NodeField(PageComment)
    node = relay.NodeField()
    all_page_links = relay.ConnectionField(PageLink)
    all_page_comments = relay.ConnectionField(PageComment)

    def resolve_all_page_links(self, args, info):
        return [PageLink.get_node()]

    def resolve_all_page_comments(self, args, info):
        return [PageComment.get_node()]

local_schema = SimpleLazyObject(lambda: graphene.Schema(query=Query))
