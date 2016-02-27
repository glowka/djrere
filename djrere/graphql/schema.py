import graphene
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from graphene import relay
from graphene.contrib.django import DjangoNode

from ..blog.schema import Blog
from ..frontpage.schema import Frontpage, Mutation as FrontpageMutation


class User(DjangoNode):
    blog = graphene.Field(Blog, resolver=(lambda self, args, info: Blog.get_from_user_id(user_id=self.id)))
    frontpage = graphene.Field(Frontpage, resolver=(lambda self, args, info: Frontpage.get_from_user_id(user_id=self.id)))

    class Meta:
        model = get_user_model()
        only_fields = ['id', 'email', 'username']

    @classmethod
    def get_node(cls, id, info=None):
        return cls.get_from_root_value(info, id)

    @classmethod
    def get_from_root_value(cls, info, user_id=None):
        user = info.root_value.get('user', None) if info else None
        if user is None:
            raise ValueError('root_value misses user data')

        if not user.is_authenticated():
            # Continue as anonymous user, fake id
            return get_user_model()(id=-1)

        if not settings.DEBUG and user_id is not None and user.pk != id:
            raise PermissionDenied('passed id does not match user id passed by root_value ')
        return user


class Query(graphene.ObjectType):
    node = relay.NodeField(relay.Node)
    user = graphene.Field(User)

    def resolve_user(self, args, info):
        return User.get_from_root_value(info)


class Mutation(FrontpageMutation):
    # blog = graphene.Field(BlogMutation)
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
