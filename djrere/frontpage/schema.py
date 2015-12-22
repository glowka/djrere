import graphene
from graphene import relay


class FrontLink(relay.Node):
    href = graphene.String()
    description = graphene.String()

    def resolve_href(self, *args, **kwargs):
        return 'http://isivi.pl'

    def resolve_description(self, *args, **kwargs):
        return 'Lepsze oferty!'

    @classmethod
    def get_node(cls, node_id, info):
        return cls(href='incivi.pl', description='Ferty')


class Query(graphene.ObjectType):
    front_link = graphene.Field(FrontLink)
    node = relay.NodeField()

    def resolve_front_link(self, *args, **kwargs):
        return FrontLink(href='incivi.pl', description='Ferty')


schema = graphene.Schema(query=Query)