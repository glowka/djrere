import graphene
from graphene import relay
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

    def resolve_content(self, *args, **kwargs):
        return getattr(self, 'content', 'content_value')

    def resolve_link(self, *args, **kwargs):
        return getattr(self, 'link', FrontLink.get_node())


class FrontLink(AwareNode):
    href = graphene.String()
    description = graphene.String()
    comments = relay.ConnectionField(Comment)

    def resolve_href(self, *args, **kwargs):
        return getattr(self, 'href', 'href_value')

    def resolve_description(self, *args, **kwargs):
        return getattr(self, 'desc', 'desc_value')

    def resolve_comments(self, *args, **kwargs):
        return [Comment.get_node()]


class Query(graphene.ObjectType):
    front_link = relay.NodeField(FrontLink)
    comment = relay.NodeField(Comment)
    node = relay.NodeField()
    all_front_links = relay.ConnectionField(FrontLink)
    all_comments = relay.ConnectionField(Comment)

    def resolve_all_front_links(self, *args, **kwargs):
        return [FrontLink.get_node()]

    def resolve_all_comments(self, *args, **kwargs):
        return [Comment.get_node()]

schema = graphene.Schema(query=Query)