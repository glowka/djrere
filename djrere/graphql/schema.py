import graphene
from graphene import relay

from djrere.frontpage.schema import FrontLink, Comment


class Query(graphene.ObjectType):
    front_link = relay.NodeField(FrontLink)
    comment = relay.NodeField(Comment)
    node = relay.NodeField()
    all_front_links = relay.ConnectionField(FrontLink)
    all_comments = relay.ConnectionField(Comment)

    def resolve_all_front_links(self, args, info):
        return [FrontLink.get_node()]

    def resolve_all_comments(self, args, info):
        return [Comment.get_node()]

schema = graphene.Schema(query=Query)