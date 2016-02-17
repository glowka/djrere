import graphene
from graphene import relay

from ..utils.query import viewer_query
from ..frontpage.schema import Query as FrontpageQuery, Mutation as FrontpageMutation
from ..blog.schema import BlogQuery, BlogMutation


class Query(FrontpageQuery):
    blog = graphene.Field(BlogQuery, resolver=lambda self, args, info: True)


class Mutation(FrontpageMutation):
    # blog = graphene.Field(BlogMutation)
    pass

schema = graphene.Schema(query=viewer_query(Query), mutation=Mutation)
