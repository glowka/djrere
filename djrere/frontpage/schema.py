# coding=utf-8
import graphene
from django.utils.functional import SimpleLazyObject
from graphene import relay
from graphene.contrib.django import DjangoNode
from graphql_relay import from_global_id, to_global_id
from graphql_relay.connection.arrayconnection import offset_to_cursor

from . import models
from ..utils.query import user_wrapped_query


class Connection(relay.Connection):
    count = graphene.IntField()

    def resolve_count(self, args, info):
        return self._connection_data.count()


class PageComment(DjangoNode):
    link = graphene.Field('PageLink')
    content = graphene.String()

    connection_type = Connection

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

    connection_type = Connection

    class Meta:
        model = models.PageLink

    def resolve_href(self, args, info):
        return self.instance.href

    def resolve_description(self, args, info):
        return self.instance.description

    def resolve_page_comments(self, args, info):
        return self.instance.page_comments.all()


class MyObject(graphene.ObjectType):
    str_content = graphene.String()
    str_length = graphene.Int()

    def resolve_str_content(self, args, info):
        return self._root

    def resolve_str_length(self, args, info):
        return len(self._root)


class Frontpage(relay.Node):
    my_str = graphene.Field(MyObject)

    page_link = relay.NodeField(PageLink)
    page_comment = relay.NodeField(PageComment)
    node = relay.NodeField()
    all_page_links = relay.ConnectionField(PageLink)
    all_page_comments = relay.ConnectionField(PageComment)

    def resolve_my_str(self, args, info):
        return 'my_str'

    def resolve_all_page_links(self, args, info):
        return models.PageLink.objects.all()

    def resolve_all_page_comments(self, args, info):
        return models.PageComment.objects.all()

    @classmethod
    def get_node(cls, id):
        return cls(id=id)

    @classmethod
    def get_from_user_id(cls, user_id):
        return cls(id=user_id)


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
        schema = info.schema.graphene_schema

        link_global_id = input.get('link_id')
        link_id = from_global_id(link_global_id).id
        # TODO: too complicated, anti-pattern and prone to mistakes way of getting offset
        offset = schema.execute(
            'query { user { frontpage { pageLink(id: "%s") { pageComments {count} } } } }' % link_global_id,
            root=info.root_value
        ).data['user']['frontpage']['pageLink']['pageComments']['count']

        comment_model = models.PageComment.objects.create(content=input.get('content'), link_id=link_id)
        comment = PageComment(comment_model)
        link_model = models.PageLink.objects.get(pk=link_id)

        return cls(success=True,
                   page_comment=comment,
                   page_comment_edge=PageComment.get_edge_type()(node=comment,
                                                                 cursor=offset_to_cursor(offset)),
                   link=PageLink(link_model))


class AddPageLink(relay.ClientIDMutation):
    class Input(object):
        href = graphene.String().NonNull
        description = graphene.String()
        user = graphene.String().NonNull

    success = graphene.Boolean()
    page_link_edge = graphene.Field(PageLink.get_edge_type().for_node(PageLink))
    link = graphene.Field(PageLink)
    frontpage = graphene.Field('Frontpage')

    @classmethod
    def mutate_and_get_payload(cls, input, info):
        schema = info.schema.graphene_schema

        user_id = from_global_id(input.get('user')).id
        Frontpage = schema.get_type('Frontpage')

        # TODO: too complicated, anti-pattern and prone to mistakes way of getting offset
        offset = schema.execute(
            'query { user { frontpage { allPageLinks { count } } } }',
            root=info.root_value
        ).data['user']['frontpage']['allPageLinks']['count']

        link_model = models.PageLink.objects.create(href=input.get('href'), description=input.get('description'))
        link = PageLink(link_model)
        return cls(success=True,
                   link=link,
                   page_link_edge=PageLink.get_edge_type().for_node(PageLink)(node=link,
                                                                              cursor=offset_to_cursor(offset)),
                   frontpage=Frontpage.get_from_user_id(user_id)
                   )


class DeletePageLink(relay.ClientIDMutation):
    class Input(object):
        page_link = graphene.String().NonNull
        user = graphene.String().NonNull

    success = graphene.Boolean()
    deletedPageLinks = graphene.List(graphene.String())
    frontpage = graphene.Field('Frontpage')

    @classmethod
    def mutate_and_get_payload(cls, input, info):
        user_id = from_global_id(input.get('user')).id

        page_link_id = from_global_id(input.get('page_link')).id
        models.PageLink.objects.filter(pk=page_link_id).delete()

        schema = info.schema.graphene_schema
        Frontpage = schema.get_type('Frontpage')

        return cls(success=True,
                   deletedPageLinks=[to_global_id(PageLink.__name__, page_link_id)],
                   frontpage=Frontpage.get_from_user_id(user_id)
                   )


class Mutation(graphene.ObjectType):
    add_page_comment = graphene.Field(AddPageComment)
    add_page_link = graphene.Field(AddPageLink)
    delete_page_link = graphene.Field(DeletePageLink)


local_schema = SimpleLazyObject(lambda: graphene.Schema(query=user_wrapped_query(Frontpage), mutation=Mutation))
