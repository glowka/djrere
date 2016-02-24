import graphene
from graphene import relay


def user_wrapped_query(query_class, resolve_user=None):

    class User(relay.Node, query_class):
        id = 0

        def get_node(self, id, info):
            return User(id=id)

    class Query(graphene.ObjectType):
        user = graphene.Field(User, id=graphene.String())
        node = relay.NodeField(relay.Node)

        def resolve_user(self, args, info):
            if resolve_user is not None:
                return resolve_user(self, args, info)
            return User()

    return Query