import json


# noinspection PyPep8Naming,PyAttributeOutsideInit
class GraphTestMixin(object):
    def setUp(self):
        # noinspection PyUnresolvedReferences
        super(GraphTestMixin, self).setUp()
        self.maxDiff = 1000

    def assertGraphQuery(self, schema, query, expected):
        result = schema.execute(query)
        # noinspection PyUnresolvedReferences
        self.assertFalse(result.errors, result.errors)
        try:
            pretty_data = json.loads(json.dumps(result.data))
        except ValueError:
            pretty_data = None
        # noinspection PyUnresolvedReferences
        self.assertDictEqual(pretty_data or result.data, expected)
