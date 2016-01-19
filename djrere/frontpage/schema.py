import graphene
from django.utils.functional import SimpleLazyObject
from graphene import relay
from graphene.contrib.django import DjangoNode
from graphql_relay import from_global_id, to_global_id

from . import models
from ..utils.query import viewer_query


class PageComment(DjangoNode):
    link = graphene.Field('PageLink')
    content = graphene.String()

    class Meta:
        model = models.PageComment

    def resolve_content(self, args, info):
        return self.instance.content

    def resolve_link(self, args, info):
        return self.instance.link

    @classmethod
    def get_edge_type(cls):
        return super(PageComment, cls).get_edge_type().for_node(cls)


class PageLink(DjangoNode):
    href = graphene.String()
    description = graphene.String()
    page_comments = relay.ConnectionField(PageComment)

    class Meta:
        model = models.PageLink

    def resolve_href(self, args, info):
        return self.instance.href

    def resolve_description(self, args, info):
        return self.instance.description

    def resolve_page_comments(self, args, info):
        return self.instance.page_comments.all()


class Query(graphene.ObjectType):
    page_link = relay.NodeField(PageLink)
    page_comment = relay.NodeField(PageComment)
    node = relay.NodeField()
    all_page_links = relay.ConnectionField(PageLink)
    all_page_comments = relay.ConnectionField(PageComment)

    def resolve_all_page_links(self, args, info):
        return models.PageLink.objects.all()

    def resolve_all_page_comments(self, args, info):
        return models.PageComment.objects.all()


class AddPageComment(relay.ClientIDMutation):
    class Input(object):
        link_id = graphene.String().NonNull
        content = graphene.String().NonNull

    success = graphene.Boolean()
    page_comment = graphene.Field(PageComment)
    page_comment_edge = graphene.Field(PageComment.get_edge_type())
    link = graphene.Field(PageLink)

    @classmethod
    def mutate_and_get_payload(cls, input, info):
        link_id = from_global_id(input.get('link_id')).id
        comment_model = models.PageComment.objects.create(content=input.get('content'), link_id=link_id)
        comment = PageComment(comment_model)
        link_model = models.PageLink.objects.get(pk=link_id)
        return cls(success=True,
                   page_comment=comment,
                   page_comment_edge=PageComment.get_edge_type()(node=comment, cursor=''),
                   link=PageLink(link_model))


class AddPageLink(relay.ClientIDMutation):
    class Input(object):
        href = graphene.String().NonNull
        description = graphene.String()
        viewer = graphene.String().NonNull

    success = graphene.Boolean()
    page_link_edge = graphene.Field(PageLink.get_edge_type().for_node(PageLink))
    link = graphene.Field(PageLink)
    viewer = graphene.Field('ViewerQuery')

    @classmethod
    def mutate_and_get_payload(cls, input, info):
        viewer_id = from_global_id(input.get('viewer')).id

        schema = info.schema.graphene_schema
        ViewerQuery = schema.get_type('ViewerQuery')

        link_model = models.PageLink.objects.create(href=input.get('href'), description=input.get('description'))
        link = PageLink(link_model)
        return cls(success=True,
                   link=link,
                   page_link_edge=PageLink.get_edge_type().for_node(PageLink)(node=link, cursor=""),
                   viewer=ViewerQuery(id=viewer_id)
                   )


class DeletePageLink(relay.ClientIDMutation):
    class Input(object):
        page_link = graphene.String().NonNull
        viewer = graphene.String().NonNull

    success = graphene.Boolean()
    deletedPageLinks = graphene.List(graphene.String())
    viewer = graphene.Field('ViewerQuery')

    @classmethod
    def mutate_and_get_payload(cls, input, info):
        viewer_id = from_global_id(input.get('viewer')).id

        page_link_id = from_global_id(input.get('page_link')).id
        models.PageLink.objects.filter(pk=page_link_id).delete()

        schema = info.schema.graphene_schema
        ViewerQuery = schema.get_type('ViewerQuery')

        return cls(success=True,
                   deletedPageLinks=[to_global_id(PageLink.__name__, page_link_id)],
                   viewer=ViewerQuery(id=viewer_id)
                   )


class Mutation(graphene.ObjectType):
    add_page_comment = graphene.Field(AddPageComment)
    add_page_link = graphene.Field(AddPageLink)
    delete_page_link = graphene.Field(DeletePageLink)


local_schema = SimpleLazyObject(lambda: graphene.Schema(query=viewer_query(Query), mutation=Mutation))
