import graphene
from graphene import relay

from ..utils.query import viewer_query
from ..frontpage.schema import Query as FrontpageQuery, Mutation as FrontpageMutation


class Query(FrontpageQuery):
    pass


class Mutation(FrontpageMutation):
    pass



schema = graphene.Schema(query=viewer_query(Query), mutation=Mutation)
