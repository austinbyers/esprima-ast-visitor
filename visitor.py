import abc
import collections
import hashlib


class UnknownNodeTypeError(Exception):
    """Raised if we encounter a node with an unknown type."""
    pass


def objectify(data):
    if data is None:
        return None
    if isinstance(data, dict):
        if 'type' not in data:
            return data
        node_class = globals().get(data['type'])
        if not node_class:
            raise UnknownNodeTypeError("Unknown type: " + data['type'])
        return node_class(data)
    if isinstance(data, list):
        return [objectify(x) for x in data]
    return data


class Node(abc.ABC):

    @abc.abstractproperty
    def fields(self):
        return []

    def __init__(self, data):
        for field in self.fields:
            setattr(self, field, objectify(data.get(field)))

    def dict(self):
        result = collections.OrderedDict({'type': self.type})
        for field in self.fields:
            val = getattr(self, field)
            if isinstance(val, Node):
                result[field] = val.dict()
            elif isinstance(val, list):
                result[field] = [x.dict() for x in val]
            else:
                result[field] = val
        return result

    def traverse(self):
        yield self
        for field in self.fields:
            val = getattr(self, field)
            if isinstance(val, Node):
                yield from val.traverse()
            elif isinstance(val, list):
                for x in val:
                    yield from x.traverse()

    @property
    def type(self):
        return self.__class__.__name__

    def type_digest(self):
        sha = hashlib.sha256()
        for n in self.traverse():
            sha.update(n.type.encode('utf-8'))
        return sha.hexdigest()


# --- AST spec: https://github.com/estree/estree/blob/master/es5.md ---
# pylint: disable=missing-docstring,multiple-statements


class Identifier(Node):
    @property
    def fields(self): return ['name']


class Literal(Node):
    @property
    def fields(self): return ['value', 'regex']


class Program(Node):
    @property
    def fields(self): return ['body']


# ========== Statements ==========


class ExpressionStatement(Node):
    @property
    def fields(self): return ['expression']


class BlockStatement(Node):
    @property
    def fields(self): return ['body']


class EmptyStatement(Node):
    @property
    def fields(self): return []


class DebuggerStatement(Node):
    @property
    def fields(self): return []


class WithStatement(Node):
    @property
    def fields(self): ['object', 'body']


# ----- Control Flow -----


class ReturnStatement(Node):
    @property
    def fields(self): return ['argument']


class LabeledStatement(Node):
    @property
    def fields(self): return ['label', 'body']


class BreakStatement(Node):
    @property
    def fields(self): return ['label']


class ContinueStatement(Node):
    @property
    def fields(self): return ['label']


# ----- Choice -----


class IfStatement(Node):
    @property
    def fields(self): return ['test', 'consequent', 'alternate']


class SwitchStatement(Node):
    @property
    def fields(self): return ['discriminant', 'cases']


class SwitchCase(Node):
    @property
    def fields(self): return ['test', 'consequent']


# ----- Exceptions -----


class ThrowStatement(Node):
    @property
    def fields(self): return ['argument']


class TryStatement(Node):
    @property
    def fields(self): return ['block', 'guardedHandlers', 'handlers', 'handler', 'finalizer']


class CatchClause(Node):
    @property
    def fields(self): return ['param', 'body']


# ----- Loops -----


class WhileStatement(Node):
    @property
    def fields(self): return ['test', 'body']


class DoWhileStatement(Node):
    @property
    def fields(self): return ['body', 'test']


class ForStatement(Node):
    @property
    def fields(self): return ['init', 'test', 'update', 'body']


class ForInStatement(Node):
    @property
    def fields(self): return ['left', 'right', 'body']


# ========== Declarations ==========


class FunctionDeclaration(Node):
    @property
    def fields(self): return ['id', 'params', 'body']


class VariableDeclaration(Node):
    @property
    def fields(self): return ['declarations']


class VariableDeclarator(Node):
    @property
    def fields(self): return ['id', 'init']



# ========== Expressions ==========


class ThisExpression(Node):
    @property
    def fields(self): return []


class ArrayExpression(Node):
    @property
    def fields(self): return ['elements']


class ObjectExpression(Node):
    @property
    def fields(self): return ['properties']


class Property(Node):
    @property
    def fields(self): return ['key', 'value', 'kind']


class FunctionExpression(Node):
    @property
    def fields(self): return ['id', 'params', 'body']


class UnaryExpression(Node):
    @property
    def fields(self): return ['operator', 'prefix', 'argument']


class UpdateExpression(Node):
    @property
    def fields(self): return ['operator', 'argument', 'prefix']


class BinaryExpression(Node):
    @property
    def fields(self): return ['operator', 'left', 'right']


class AssignmentExpression(Node):
    @property
    def fields(self): return ['operator', 'left', 'right']


class LogicalExpression(Node):
    @property
    def fields(self): return ['operator', 'left', 'right']


class MemberExpression(Node):
    @property
    def fields(self): return ['object', 'property', 'computed']


class ConditionalExpression(Node):
    @property
    def fields(self): return ['test', 'consequent', 'alternate']


class CallExpression(Node):
    @property
    def fields(self): return ['callee', 'arguments']


class NewExpression(Node):
    @property
    def fields(self): return ['callee', 'arguments']


class SequenceExpression(Node):
    @property
    def fields(self): return ['expressions']
