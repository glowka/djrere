import graphene
from graphene import relay


def viewer_query(query_class, resolve_viewer=None):

    class ViewerQuery(relay.Node, query_class):
        id = 0

        def get_node(self, id, info):
            return ViewerQuery(id=id)

    class Query(graphene.ObjectType):
        viewer = graphene.Field(ViewerQuery, id=graphene.String())
        node = relay.NodeField(relay.Node)

        def resolve_viewer(self, args, info):
            if resolve_viewer is not None:
                return resolve_viewer(self, args, info)
            return ViewerQuery()

    return Query