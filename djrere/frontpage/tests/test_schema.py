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
                viewer {
                    pageLink(id: "%s") {
                        id,
                        href
                    }
                }
            }
            ''' % link_gid
        expected = {
            'viewer': {
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
                viewer {
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
            'viewer': {
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
                viewer {
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
            'viewer': {
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
                viewer {
                    pageComment(id: "%s") {
                        id,
                        content,
                        link { id }
                    }
                }
            }
            ''' % comment_gid
        expected = {
            'viewer': {
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
                viewer {
                    allPageLinks {
                        edges {
                            node {id}
                        }
                    }
                }
            }
            '''
        expected = {
            'viewer': {
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
                viewer {
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
            'viewer': {
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
        viewer_gid = to_global_id('ViewerQuery', '0')

        query = '''
            mutation {
                addPageLink(input: {clientMutationId: "mutation1", viewer: "%s", href: "%s", description: "%s"}) {
                    success,
                    pageLinkEdge {
                        node {
                            href, description
                        }
                    },
                    viewer { id }
                }
            }
            ''' % (viewer_gid, href, description)
        expected = {
            'addPageLink': {
                'success': True,
                'pageLinkEdge': {
                    'node': {
                        'href': href,
                        'description': description
                    }
                },
                'viewer': {
                    'id': viewer_gid
                }
            }
        }
        self.assertGraphQuery(schema, query, expected)

    def test_delete_page_link(self):
        link = self.create_page_link()
        link_gid = to_global_id(link.__class__.__name__, link.pk)
        viewer_gid = to_global_id('ViewerQuery', '0')

        query = '''
            mutation {
                deletePageLink(input: {clientMutationId: "mutation1", viewer: "%s", pageLink: "%s"}) {
                    success,
                    deletedPageLinks,
                    viewer { id }
                }
            }
            ''' % (viewer_gid, link_gid)
        expected = {
            'deletePageLink': {
                'success': True,
                'deletedPageLinks': [link_gid],
                'viewer': {
                    'id': viewer_gid
                }
            }
        }

        self.assertGraphQuery(schema, query, expected)