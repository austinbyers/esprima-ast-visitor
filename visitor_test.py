"""Test the AST traversal."""
import gzip
import json
import unittest

import visitor


class TestTraverse(unittest.TestCase):
    """Verify that traversals progress in the correct order and terminate.

    Test cases are drawn from a variety of very large real-world JS examples,
    including popular libraries and code served by the Alexa top 10.
    """

    def _test_ast_file(self, path: str) -> None:
        """Traverse the AST specified in the given test file."""
        with gzip.open(path, 'rt') as ast_file:
            ast_string = ast_file.read()

        # The expected traversal is given by the layout of the JSON file.
        expected_types = []
        for line in ast_string.split('\n'):
            words = line.strip().split()
            if words[0] == '"type":':
                expected_types.append(words[1].strip(',').strip('"'))

        # Traverse the AST, keeping track of node types.
        node = visitor.Program(json.loads(ast_string))
        found_types = [n.type for n in node.traverse()]

        self.assertEqual(expected_types, found_types)

        # Dump the node back to a dict and make sure it parses again the same way.
        reparsed = visitor.Program(node.dict())
        newfound_types = [n.type for n in reparsed.traverse()]
        self.assertEqual(expected_types, newfound_types)

    # pylint: disable=missing-docstring

    def test_amazon(self):
        self._test_ast_file('test_ast/amazon.ast.gz')

    def test_baidu(self):
        self._test_ast_file('test_ast/baidu.ast.gz')

    def test_facebook(self):
        self._test_ast_file('test_ast/facebook.ast.gz')

    def test_google(self):
        self._test_ast_file('test_ast/google.ast.gz')

    def test_handlebars(self):
        self._test_ast_file('test_ast/handlebars.ast.gz')

    def test_jquery(self):
        self._test_ast_file('test_ast/jquery.ast.gz')

    def test_jquery_ui(self):
        self._test_ast_file('test_ast/jquery-ui.ast.gz')

    def test_qq(self):
        self._test_ast_file('test_ast/qq.ast.gz')

    def test_sugar(self):
        self._test_ast_file('test_ast/sugar.ast.gz')

    def test_twitter(self):
        self._test_ast_file('test_ast/twitter.ast.gz')

    def test_wikipedia(self):
        self._test_ast_file('test_ast/wikipedia.ast.gz')

    def test_yahoo(self):
        self._test_ast_file('test_ast/yahoo.ast.gz')

    def test_remaining(self):
        """Test any node types which weren't already covered."""
        data = {
            'type': 'WithStatement',
            'object': None,
            'body': {
                'type': 'DebuggerStatement'
            }
        }
        node = visitor.objectify(data)
        self.assertEqual(
            ['WithStatement', 'DebuggerStatement'], [n.type for n in node.traverse()])

    def test_unexpected_node_type(self):
        """Verify traversal failure for an unknown node type."""
        with self.assertRaises(visitor.UnknownNodeTypeError):
            visitor.objectify({'type': 'FakeNodeType'})


if __name__ == '__main__':
    unittest.main()
