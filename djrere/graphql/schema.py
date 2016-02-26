import graphene
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from graphene import relay

from ..blog.schema import Blog
from ..frontpage.schema import Frontpage, Mutation as FrontpageMutation


class User(relay.Node):
    blog = graphene.Field(Blog, resolver=(lambda self, args, info: Blog.get_from_user_id(user_id=self.id)))
    frontpage = graphene.Field(Frontpage, resolver=(lambda self, args, info: Frontpage.get_from_user_id(user_id=self.id)))

    @classmethod
    def get_node(cls, id, info):
        return cls.get_from_root_value(info, user_id=id)

    @classmethod
    def get_from_root_value(cls, info, user_id=None):
        user = info.root_value.get('user', None)
        if user is None:
            raise ValueError('root_value misses user data')
        user_model = get_user_model()

        if not user.is_authenticated():
            # Continue as anonymous user
            return cls(id=-1)

        if id is not None and user.pk != id:
            raise PermissionDenied('passed id does not match user id passed by root_value ')

        try:
            return cls(user, id=user.pk)
        except user_model.DoesNotExist:
            raise ValueError('user passed by root_value does not exist')


class Query(graphene.ObjectType):
    node = relay.NodeField(relay.Node)
    user = graphene.Field(User)

    def resolve_user(self, args, info):
        return User.get_from_root_value(info)


class Mutation(FrontpageMutation):
    # blog = graphene.Field(BlogMutation)
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
