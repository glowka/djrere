import graphene

from ..frontpage.schema import Query as FrontpageQuery


class Query(FrontpageQuery):
    pass

schema = graphene.Schema(query=Query)
