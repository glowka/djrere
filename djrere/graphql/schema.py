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

        if settings.DEBUG and user_id is not None:
            return get_user_model().objects.get(pk=user_id)

        if not user.is_authenticated():
            raise PermissionDenied('only authenticated user can access User node')

        if user_id is not None and user.pk != user_id:
            raise PermissionDenied('passed id does not match user id passed by root_value ')
        return user


class Query(graphene.ObjectType):
    user = graphene.Field(User, args={'id': graphene.Int()})
    node = relay.NodeField(relay.Node)

    # noinspection PyMethodMayBeStatic
    def resolve_user(self, args, info):
        return User.get_from_root_value(info, user_id=args.get('id', None))


class Mutation(FrontpageMutation):
    # blog = graphene.Field(BlogMutation)
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
