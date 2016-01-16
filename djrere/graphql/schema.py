import graphene
from graphene import relay

from ..frontpage.schema import Query as FrontpageQuery, Mutation as FrontpageMutation


class Query(FrontpageQuery):
    pass


class Mutation(FrontpageMutation):
    pass


def viewer_query(query_class):

    class ViewerQuery(relay.Node, query_class):
        id = 0

        def get_node(self, id, info):
            return ViewerQuery(id=id)

    class Query(graphene.ObjectType):
        viewer = graphene.Field(ViewerQuery, id=graphene.Int())
        node = relay.NodeField(relay.Node)

        def resolve_viewer(self, args, info):
            return ViewerQuery()

    return Query

schema = graphene.Schema(query=viewer_query(Query), mutation=Mutation)
