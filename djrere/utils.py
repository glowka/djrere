import collections

import graphene
from graphene import relay


def update_recursive(d, u):
    """
    Update dict in recursive manner.

    :param d: dict to be updated
    :param u: dict containing values d will be updated with
    """
    for k in u.keys():
        if isinstance(u[k], collections.Mapping) and isinstance(d.get(k, None), collections.Mapping):
            update_recursive(d[k], u[k])
        else:
            d[k] = u[k]


def viewer_query(query_class, resolve_viewer=None):

    class ViewerQuery(relay.Node, query_class):
        id = 0

        def get_node(self, id_, info):
            return ViewerQuery(id=id_)

    class Query(graphene.ObjectType):
        viewer = graphene.Field(ViewerQuery, id=graphene.String())
        node = relay.NodeField(relay.Node)

        def resolve_viewer(self, args, info):
            if resolve_viewer is not None:
                return resolve_viewer(self, args, info)
            return ViewerQuery()

    return Query