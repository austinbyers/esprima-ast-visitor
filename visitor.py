"""Esprima AST Node Visitor.

Usage:
    for node in traverse(json.loads(esprima_ast_string)):
        print(node['type'])
        # Do other work with node
"""
# Austin Byers, 2016

class UnknownNodeTypeError(Exception):
    """Raised if we encounter a node with an unknown type."""
    pass

def traverse(node):
    """Recursive pre-order AST traversal.

    Args:
        node: A dictionary representing an Esprima AST node.
    """
    yield node

    child_generator = globals().get('_traverse_' + node['type'])
    if child_generator is not None:
        yield from child_generator(node)
    else:
        raise UnknownNodeTypeError(node['type'])

# ~~~~~ AST Spec: https://github.com/estree/estree/blob/master/spec.md ~~~~~
def _traverse_Identifier(node):
    yield from ()

def _traverse_Literal(node):
    yield from ()

def _traverse_Program(node):
    for b in node['body']:
        yield from traverse(b)

##### Statements #####
def _traverse_ExpressionStatement(node):
    yield from traverse(node['expression'])

def _traverse_BlockStatement(node):
    for b in node['body']:
        yield from traverse(b)

def _traverse_EmptyStatement(node):
    yield from ()

def _traverse_DebuggerStatement(node):
    yield from ()

def _traverse_WithStatement(node):
    yield from traverse(node['object'])
    yield from traverse(node['body'])

### Control Flow ###
def _traverse_ReturnStatement(node):
    if node['argument'] is not None:
        yield from traverse(node['argument'])

def _traverse_LabeledStatement(node):
    yield from traverse(node['label'])
    yield from traverse(node['body'])

def _traverse_BreakStatement(node):
    if node['label'] is not None:
        yield from traverse(node['label'])

def _traverse_ContinueStatement(node):
    if node['label'] is not None:
        yield from traverse(node['label'])

### Choice ###
def _traverse_IfStatement(node):
    yield from traverse(node['test'])
    yield from traverse(node['consequent'])
    if node['alternate'] is not None:
        yield from traverse(node['alternate'])

def _traverse_SwitchStatement(node):
    yield from traverse(node['discriminant'])
    for c in node['cases']:
        yield from traverse(c)

def _traverse_SwitchCase(node):
    if node['test'] is not None:
        yield from traverse(node['test'])
    for c in node['consequent']:
        yield from traverse(c)

### Exceptions ###
def _traverse_ThrowStatement(node):
    yield from traverse(node['argument'])

# Note: the "guardedHandlers" and "handlers" fields aren't in the spec.
def _traverse_TryStatement(node):
    yield from traverse(node['block'])
    for h in node['guardedHandlers']:
        yield from traverse(h)
    for h in node['handlers']:
        yield from traverse(h)
    if node['handler'] is not None:
        yield from traverse(node['handler'])
    if node['finalizer'] is not None:
        yield from traverse(node['finalizer'])

def _traverse_CatchClause(node):
    yield from traverse(node['param'])
    yield from traverse(node['body'])

### Loops ###
def _traverse_WhileStatement(node):
    yield from traverse(node['test'])
    yield from traverse(node['body'])

def _traverse_DoWhileStatement(node):
    yield from traverse(node['body'])
    yield from traverse(node['test'])

def _traverse_ForStatement(node):
    if node['init'] is not None:
        yield from traverse(node['init'])
    if node['test'] is not None:
        yield from traverse(node['test'])
    if node['update'] is not None:
        yield from traverse(node['update'])
    yield from traverse(node['body'])

def _traverse_ForInStatement(node):
    yield from traverse(node['left'])
    yield from traverse(node['right'])
    yield from traverse(node['body'])

##### Declarations #####
def _traverse_FunctionDeclaration(node):
    yield from traverse(node['id'])
    for p in node['params']:
        yield from traverse(p)
    yield from traverse(node['body'])

def _traverse_VariableDeclaration(node):
    for d in node['declarations']:
        yield from traverse(d)

def _traverse_VariableDeclarator(node):
    yield from traverse(node['id'])
    if node['init'] is not None:
        yield from traverse(node['init'])

##### Expressions #####
def _traverse_ThisExpression(node):
    yield from ()

def _traverse_ArrayExpression(node):
    for e in node['elements']:
        yield from traverse(e)

def _traverse_ObjectExpression(node):
    for p in node['properties']:
        yield from traverse(p)

def _traverse_Property(node):
    yield from traverse(node['key'])
    yield from traverse(node['value'])

def _traverse_FunctionExpression(node):
    if node['id'] is not None:
        yield from traverse(node['id'])
    for p in node['params']:
        yield from traverse(p)
    yield from traverse(node['body'])

### Unary Operations ###
def _traverse_UnaryExpression(node):
    yield from traverse(node['argument'])

def _traverse_UpdateExpression(node):
    yield from traverse(node['argument'])

### Binary Operations ###
def _traverse_BinaryExpression(node):
    yield from traverse(node['left'])
    yield from traverse(node['right'])

def _traverse_AssignmentExpression(node):
    yield from traverse(node['left'])
    yield from traverse(node['right'])

def _traverse_LogicalExpression(node):
    yield from traverse(node['left'])
    yield from traverse(node['right'])

def _traverse_MemberExpression(node):
    yield from traverse(node['object'])
    yield from traverse(node['property'])

# Note: The spec actually puts the altnerate before the consequent.
# We use the form that Esprima generates.
def _traverse_ConditionalExpression(node):
    yield from traverse(node['test'])
    yield from traverse(node['consequent'])
    yield from traverse(node['alternate'])

def _traverse_CallExpression(node):
    yield from traverse(node['callee'])
    for a in node['arguments']:
        yield from traverse(a)

def _traverse_NewExpression(node):
    yield from _traverse_CallExpression(node)

def _traverse_SequenceExpression(node):
    for e in node['expressions']:
        yield from traverse(e)
