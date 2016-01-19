import graphene
from django.utils.functional import SimpleLazyObject
from graphene import relay
from graphene.contrib.django import DjangoNode
from graphql_relay import from_global_id, to_global_id

from . import models
from ..utils.query import viewer_query


class Comment(DjangoNode):
    link = graphene.Field('FrontLink')
    content = graphene.String()

    class Meta:
        model = models.Comment

    def resolve_content(self, args, info):
        return self.instance.content

    def resolve_link(self, args, info):
        return self.instance.link

    @classmethod
    def get_edge_type(cls):
        return super(Comment, cls).get_edge_type().for_node(cls)


class FrontLink(DjangoNode):
    href = graphene.String()
    description = graphene.String()
    comments = relay.ConnectionField(Comment)

    class Meta:
        model = models.FrontLink

    def resolve_href(self, args, info):
        return self.instance.href

    def resolve_description(self, args, info):
        return self.instance.description

    def resolve_comments(self, args, info):
        return self.instance.comments.all()


class Query(graphene.ObjectType):
    front_link = relay.NodeField(FrontLink)
    comment = relay.NodeField(Comment)
    node = relay.NodeField()
    all_front_links = relay.ConnectionField(FrontLink)
    all_comments = relay.ConnectionField(Comment)

    def resolve_all_front_links(self, args, info):
        return models.FrontLink.objects.all()

    def resolve_all_comments(self, args, info):
        return models.Comment.objects.all()


class AddComment(relay.ClientIDMutation):
    class Input(object):
        link_id = graphene.String().NonNull
        content = graphene.String().NonNull

    success = graphene.BooleanField()
    comment = graphene.Field(Comment)
    comment_edge = graphene.Field(Comment.get_edge_type())
    link = graphene.Field(FrontLink)

    @classmethod
    def mutate_and_get_payload(cls, input, info):
        link_id = from_global_id(input.get('link_id')).id
        comment_model = models.Comment.objects.create(content=input.get('content'), link_id=link_id)
        comment = Comment(comment_model)
        link_model = models.FrontLink.objects.get(pk=link_id)
        return cls(success=True,
                   comment=comment,
                   comment_edge=Comment.get_edge_type()(node=comment, cursor=''),
                   link=FrontLink(link_model))


class AddFrontLink(relay.ClientIDMutation):
    class Input(object):
        href = graphene.String().NonNull
        description = graphene.String()
        viewer = graphene.String().NonNull

    success = graphene.BooleanField()
    front_link_edge = graphene.Field(FrontLink.get_edge_type().for_node(FrontLink))
    link = graphene.Field(FrontLink)
    viewer = graphene.Field('ViewerQuery')

    @classmethod
    def mutate_and_get_payload(cls, input, info):
        viewer_id = from_global_id(input.get('viewer')).id

        schema = info.schema.graphene_schema
        ViewerQuery = schema.get_type('ViewerQuery')

        link_model = models.FrontLink.objects.create(href=input.get('href'), description=input.get('description'))
        link = FrontLink(link_model)
        return cls(success=True,
                   link=link,
                   front_link_edge=FrontLink.get_edge_type().for_node(FrontLink)(node=link, cursor=""),
                   viewer=ViewerQuery(id=viewer_id)
                   )


class DeleteFrontLink(relay.ClientIDMutation):
    class Input(object):
        front_link = graphene.String().NonNull
        viewer = graphene.String().NonNull

    success = graphene.BooleanField()
    deletedFrontLinks = graphene.List(graphene.String())
    viewer = graphene.Field('ViewerQuery')

    @classmethod
    def mutate_and_get_payload(cls, input, info):
        viewer_id = from_global_id(input.get('viewer')).id

        front_link_id = from_global_id(input.get('front_link')).id
        models.FrontLink.objects.filter(pk=front_link_id).delete()

        schema = info.schema.graphene_schema
        ViewerQuery = schema.get_type('ViewerQuery')

        return cls(success=True,
                   deletedFrontLinks=[to_global_id(FrontLink.__name__, front_link_id)],
                   viewer=ViewerQuery(id=viewer_id)
                   )


class Mutation(graphene.ObjectType):
    add_comment = graphene.Field(AddComment)
    add_front_link = graphene.Field(AddFrontLink)
    delete_front_link = graphene.Field(DeleteFrontLink)


local_schema = SimpleLazyObject(lambda: graphene.Schema(query=viewer_query(Query), mutation=Mutation))
