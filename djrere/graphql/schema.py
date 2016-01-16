import graphene

from ..frontpage.schema import Query as FrontpageQuery, Mutation as FrontpageMutation


class Query(FrontpageQuery):
    pass


class Mutation(FrontpageMutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
