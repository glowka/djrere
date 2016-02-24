from django.test import TestCase, Client
from graphql_relay import to_global_id

from ...utils.test_cases import GraphTestMixin
from ..schema import local_schema as schema
from .. import models


class SchemaTests(GraphTestMixin, TestCase):
    def setUp(self):
        super(SchemaTests, self).setUp()
        self.client = Client()

    def create_page_link(self):
        return models.PageLink.objects.create(href='www.example.com', description='description text')

    def create_page_comment(self, link):
        return models.PageComment.objects.create(link=link, content='content text')

    def test_page_link(self):
        link = self.create_page_link()
        link_gid = to_global_id(link.__class__.__name__, link.pk)
        query = '''
            query FetchPageLink {
                user {
                    pageLink(id: "%s") {
                        id,
                        href
                    }
                }
            }
            ''' % link_gid
        expected = {
            'user': {
                'pageLink': {
                    'id': link_gid,
                    'href': link.href
                }
            }
        }

        self.assertGraphQuery(schema, query, expected)

    def test_page_link_comments(self):
        link = self.create_page_link()
        comment = self.create_page_comment(link)
        link_gid = to_global_id(link.__class__.__name__, link.pk)
        comment_gid = to_global_id(comment.__class__.__name__, comment.pk)

        query = '''
            query FetchPageLink {
                user {
                    pageLink(id: "%s") {
                        id,
                        pageComments {
                            edges {
                                node { id }
                            }
                        }
                    }
                }
            }
            ''' % link_gid

        expected = {
            'user': {
                'pageLink': {
                    'id': link_gid,
                    'pageComments': {
                        'edges': [
                            {'node': {'id': comment_gid}}
                        ]
                    }
                }
            }
        }

        self.assertGraphQuery(schema, query, expected)

    def test_page_link_comments_deep(self):
        link = self.create_page_link()
        comment = self.create_page_comment(link)
        link_gid = to_global_id(link.__class__.__name__, link.pk)
        comment_gid = to_global_id(comment.__class__.__name__, comment.pk)

        query = '''
            query FetchPageLink {
                user {
                    pageLink(id: "%s") {
                        id,
                        pageComments {
                            edges {
                                node {
                                    id,
                                    link { id }
                                }
                            }
                        }
                    }
                }
            }
            ''' % link_gid

        expected = {
            'user': {
                'pageLink': {
                    'id': link_gid,
                    'pageComments': {
                        'edges': [
                            {
                                'node': {
                                    'id': comment_gid,
                                    'link': {'id': link_gid}
                                }
                            }
                        ]
                    }
                }
            }
        }

        self.assertGraphQuery(schema, query, expected)

    def test_page_comment(self):
        link = self.create_page_link()
        link_gid = to_global_id(link.__class__.__name__, link.pk)
        comment = self.create_page_comment(link)
        comment_gid = to_global_id(comment.__class__.__name__, comment.pk)

        query = '''
            query FetchPageComment {
                user {
                    pageComment(id: "%s") {
                        id,
                        content,
                        link { id }
                    }
                }
            }
            ''' % comment_gid
        expected = {
            'user': {
                'pageComment': {
                    'id': comment_gid,
                    'content': comment.content,
                    'link': {'id': link_gid}
                }
            }
        }

        self.assertGraphQuery(schema, query, expected)

    def test_all_page_links(self):
        link = self.create_page_link()
        link_gid = to_global_id(link.__class__.__name__, link.pk)

        query = '''
            query FetchAllPageLinks {
                user {
                    allPageLinks {
                        edges {
                            node {id}
                        }
                    }
                }
            }
            '''
        expected = {
            'user': {
                'allPageLinks': {
                    'edges': [
                        {'node': {'id': link_gid}}
                    ]
                }
            }
        }

        self.assertGraphQuery(schema, query, expected)

    def test_all_comments(self):
        link = self.create_page_link()
        link_gid = to_global_id(link.__class__.__name__, link.pk)
        comment = self.create_page_comment(link)
        comment_gid = to_global_id(comment.__class__.__name__, comment.pk)

        query = '''
            query FetchAllPageComments {
                user {
                    allPageComments {
                        edges {
                            node {
                                id,
                                content,
                                link { id }
                            }
                        }
                    }
                }
            }
            '''
        expected = {
            'user': {
                'allPageComments': {
                    'edges': [
                        {
                            'node': {
                                'id': comment_gid,
                                'content': comment.content,
                                'link': {'id': link_gid}
                            }
                        }
                    ]
                }
            }
        }

        self.assertGraphQuery(schema, query, expected)

    def test_add_page_comment(self):
        link = self.create_page_link()
        link_gid = to_global_id(link.__class__.__name__, link.pk)
        comment_content = 'test content'

        query = '''
            mutation {
                addPageComment(input: {clientMutationId: "mutation1", linkId: "%s", content: "%s"}) {
                    success,
                    pageCommentEdge {
                        node {
                            content, link { id }
                        }
                    },
                    link { id }


                }
            }
            ''' % (link_gid, comment_content)
        expected = {
            'addPageComment': {
                'success': True,
                'pageCommentEdge': {
                    'node': {
                        'content': comment_content,
                        'link': {'id': link_gid}
                    }
                },
                'link': {
                    'id': link_gid
                }
            }
        }

        self.assertGraphQuery(schema, query, expected)

    def test_add_page_link(self):
        href = 'www.example.com'
        description = 'description text'
        user_gid = to_global_id('User', '0')

        query = '''
            mutation {
                addPageLink(input: {clientMutationId: "mutation1", user: "%s", href: "%s", description: "%s"}) {
                    success,
                    pageLinkEdge {
                        node {
                            href, description
                        }
                    },
                    user { id }
                }
            }
            ''' % (user_gid, href, description)
        expected = {
            'addPageLink': {
                'success': True,
                'pageLinkEdge': {
                    'node': {
                        'href': href,
                        'description': description
                    }
                },
                'user': {
                    'id': user_gid
                }
            }
        }
        self.assertGraphQuery(schema, query, expected)

    def test_delete_page_link(self):
        link = self.create_page_link()
        link_gid = to_global_id(link.__class__.__name__, link.pk)
        user_gid = to_global_id('User', '0')

        query = '''
            mutation {
                deletePageLink(input: {clientMutationId: "mutation1", user: "%s", pageLink: "%s"}) {
                    success,
                    deletedPageLinks,
                    user { id }
                }
            }
            ''' % (user_gid, link_gid)
        expected = {
            'deletePageLink': {
                'success': True,
                'deletedPageLinks': [link_gid],
                'user': {
                    'id': user_gid
                }
            }
        }

        self.assertGraphQuery(schema, query, expected)