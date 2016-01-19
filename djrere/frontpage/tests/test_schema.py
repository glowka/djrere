from django.test import TestCase, Client
from graphql_relay import to_global_id

from ...utils.test_cases import GraphTestMixin
from ..schema import local_schema as schema
from .. import models


class SchemaTests(GraphTestMixin, TestCase):
    def setUp(self):
        super(SchemaTests, self).setUp()
        self.client = Client()

    def create_front_link(self):
        return models.FrontLink.objects.create(href='www.example.com', description='description text')

    def create_comment(self, link):
        return models.Comment.objects.create(link=link, content='content text')

    def test_front_link(self):
        link = self.create_front_link()
        link_gid = to_global_id(link.__class__.__name__, link.pk)
        query = '''
            query FetchFrontLink {
                viewer {
                    frontLink(id: "%s") {
                        id,
                        href
                    }
                }
            }
            ''' % link_gid
        expected = {
            'viewer': {
                'frontLink': {
                    'id': link_gid,
                    'href': link.href
                }
            }
        }

        self.assertGraphQuery(schema, query, expected)

    def test_front_link_comments(self):
        link = self.create_front_link()
        comment = self.create_comment(link)
        link_gid = to_global_id(link.__class__.__name__, link.pk)
        comment_gid = to_global_id(comment.__class__.__name__, comment.pk)

        query = '''
            query FetchFrontLink {
                viewer {
                    frontLink(id: "%s") {
                        id,
                        comments {
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
                'frontLink': {
                    'id': link_gid,
                    'comments': {
                        'edges': [
                            {'node': {'id': comment_gid}}
                        ]
                    }
                }
            }
        }

        self.assertGraphQuery(schema, query, expected)

    def test_front_link_comments_deep(self):
        link = self.create_front_link()
        comment = self.create_comment(link)
        link_gid = to_global_id(link.__class__.__name__, link.pk)
        comment_gid = to_global_id(comment.__class__.__name__, comment.pk)

        query = '''
            query FetchFrontLink {
                viewer {
                    frontLink(id: "%s") {
                        id,
                        comments {
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
                'frontLink': {
                    'id': link_gid,
                    'comments': {
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

    def test_comment(self):
        link = self.create_front_link()
        link_gid = to_global_id(link.__class__.__name__, link.pk)
        comment = self.create_comment(link)
        comment_gid = to_global_id(comment.__class__.__name__, comment.pk)

        query = '''
            query FetchComment {
                viewer {
                    comment(id: "%s") {
                        id,
                        content,
                        link { id }
                    }
                }
            }
            ''' % comment_gid
        expected = {
            'viewer': {
                'comment': {
                    'id': comment_gid,
                    'content': comment.content,
                    'link': {'id': link_gid}
                }
            }
        }

        self.assertGraphQuery(schema, query, expected)

    def test_all_front_links(self):
        link = self.create_front_link()
        link_gid = to_global_id(link.__class__.__name__, link.pk)

        query = '''
            query FetchAllFrontLinks {
                viewer {
                    allFrontLinks {
                        edges {
                            node {id}
                        }
                    }
                }
            }
            '''
        expected = {
            'viewer': {
                'allFrontLinks': {
                    'edges': [
                        {'node': {'id': link_gid}}
                    ]
                }
            }
        }

        self.assertGraphQuery(schema, query, expected)

    def test_all_comments(self):
        link = self.create_front_link()
        link_gid = to_global_id(link.__class__.__name__, link.pk)
        comment = self.create_comment(link)
        comment_gid = to_global_id(comment.__class__.__name__, comment.pk)

        query = '''
            query FetchAllComments {
                viewer {
                    allComments {
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
                'allComments': {
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

    def test_add_comment(self):
        link = self.create_front_link()
        link_gid = to_global_id(link.__class__.__name__, link.pk)
        comment_content = 'test content'

        query = '''
            mutation {
                addComment(input: {clientMutationId: "mutation1", linkId: "%s", content: "%s"}) {
                    success,
                    commentEdge {
                        node {
                            content, link { id }
                        }
                    },
                    link { id }


                }
            }
            ''' % (link_gid, comment_content)
        expected = {
            'addComment': {
                'success': True,
                'commentEdge': {
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

    def test_add_front_link(self):
        href = 'www.example.com'
        description = 'description text'
        viewer_gid = to_global_id('ViewerQuery', '0')

        query = '''
            mutation {
                addFrontLink(input: {clientMutationId: "mutation1", viewer: "%s", href: "%s", description: "%s"}) {
                    success,
                    frontLinkEdge {
                        node {
                            href, description
                        }
                    },
                    viewer { id }
                }
            }
            ''' % (viewer_gid, href, description)
        expected = {
            'addFrontLink': {
                'success': True,
                'frontLinkEdge': {
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

    def test_delete_front_link(self):
        link = self.create_front_link()
        link_gid = to_global_id(link.__class__.__name__, link.pk)
        viewer_gid = to_global_id('ViewerQuery', '0')

        query = '''
            mutation {
                deleteFrontLink(input: {clientMutationId: "mutation1", viewer: "%s", frontLink: "%s"}) {
                    success,
                    deletedFrontLinks,
                    viewer { id }
                }
            }
            ''' % (viewer_gid, link_gid)
        expected = {
            'deleteFrontLink': {
                'success': True,
                'deletedFrontLinks': [link_gid],
                'viewer': {
                    'id': viewer_gid
                }
            }
        }

        self.assertGraphQuery(schema, query, expected)