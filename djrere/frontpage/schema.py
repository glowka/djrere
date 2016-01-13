import graphene
from django.utils.functional import SimpleLazyObject
from graphene import relay

from . import models


class AwareEdge(relay.Edge):
    def resolve_node(self, args, info):
        return self.node_type(self.node)


class AwareNode(relay.Node):
    class Meta:
        abstract = True

    def __init__(self, root):
        super(AwareNode, self).__init__()
        self.root = root
        self.id = self.root.pk

    edge_type = AwareEdge
    

class Comment(AwareNode):
    link = graphene.Field('FrontLink')
    content = graphene.String()

    def resolve_content(self, args, info):
        return self.root.content

    def resolve_link(self, args, info):
        return self.root.link

    @classmethod
    def get_node(cls, local_id, info=None):
        return Comment.objects.get(pk=local_id)



class FrontLink(AwareNode):
    href = graphene.String()
    description = graphene.String()
    comments = relay.ConnectionField(Comment)

    def resolve_href(self, args, info):
        return self.root.href

    def resolve_description(self, args, info):
        return self.root.description

    def resolve_comments(self, args, info):
        return self.root.comments.all()

    @classmethod
    def get_node(cls, local_id, info=None):
        return FrontLink.objects.get(pk=local_id)




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
