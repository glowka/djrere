import traceback

import graphene
from graphene import relay
from graphene.contrib import django as django_relay
from graphql_relay import to_global_id, from_global_id


def get_node(global_id):
    node_class, local_id = from_global_id(global_id)
    node_class(id=global_id)


class AwareNode(relay.Node):
    class Meta:
        abstract = True

    @classmethod
    def get_node(cls, local_id=1, info=None):
        return cls(id=local_id)


class Comment(AwareNode):
    link = graphene.Field('FrontLink')
    content = graphene.String()

    def resolve_content(self, args, info):
        return getattr(self, 'content', 'content_value')

    def resolve_link(self, args, info):
        return getattr(self, 'link', FrontLink.get_node())


class FrontLink(AwareNode):
    href = graphene.String()
    description = graphene.String()
    comments = relay.ConnectionField(Comment)

    def resolve_href(self, args, info):
        return getattr(self, 'href', 'href_value')

    def resolve_description(self, args, info):
        return getattr(self, 'desc', 'desc_value')

    def resolve_comments(self, args, info):
        return [Comment.get_node()]

