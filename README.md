# Esprima Abstract Syntax Tree (AST) Visitor
[![Build Status](https://travis-ci.org/austinbyers/esprima-ast-visitor.svg?branch=master)](https://travis-ci.org/austinbyers/esprima-ast-visitor)
[![Coverage Status](https://coveralls.io/repos/github/austinbyers/esprima-ast-visitor/badge.svg?branch=master)](https://coveralls.io/github/austinbyers/esprima-ast-visitor?branch=master)


This is a Python3.5+ module for transforming an Esprima AST into a traversable Python object.

## JavaScript Parsing with Esprima
[Esprima](http://esprima.org/) is a popular state-of-the-art JavaScript parser.
You can use Esprima's [nodejs package](https://www.npmjs.com/package/esprima)
to parse a JavaScript file and output it's Abstract Syntax Tree (AST) as a JSON file:

```javascript
var esprima = require('esprima');
JSON.stringify(esprima.parse(js_string), null, 2);
```

## AST Format
Esprima's AST follows a [standard format](https://github.com/estree/estree/blob/master/es5.md) specified by the [ESTree project](https://github.com/estree/estree).
While there are other nodejs projects that provide Esprima AST traversal
(e.g. [estraverse](https://github.com/estools/estraverse)), I was unable
to find an equivalent Python tool. So I made one myself!

## Usage
```python
import json

import visitor

ast = json.loads(esprima_ast_string)
program = visitor.objectify(ast)  # visitor.Node object

for node in program.traverse():
    print(node.type)
    # Replace all return statements with 'return null'
    if node.type == 'ReturnStatement':
        node.argument = None

# Save modified tree back to JSON format
with open('modified_ast.json', 'w') as f:
    f.write(json.dumps(node.dict(), indent=2))
```

## `Node` Properties
Every component of the parsed AST is a subclass of `visitor.Node`. Every node has the following properties:

```python
node = visitor.objectify('your-json-ast-string')

node.fields      # List of available attributes for this specific node (e.g. ['key', 'value']).
                 #     Node fields can be accessed directly (e.g. node.key, node.value)
node.type        # Class name (e.g. "Program" or "VariableDeclarator")
node.dict()      # Transform Node back into an AST dictionary
node.traverse()  # Pre-order traversal of this node and its children (which may also be Node objects)
```

## A Complete Example
Suppose we want to traverse the following JS code:

```js
var map = {'abc': 123}
```

First, we can use Esprima to get the AST (in JSON) format, like so:
```bash
$ npm install esprima
$ node
> var esprima = require('esprima');
> var fs = require('fs');
> ast_string = JSON.stringify(esprima.parse("var map = {'abc': 123}"), null, 2);
> fs.writeFile('test.json', ast_string, null);
```

Then, we can load it into traversable Node objects:

```python
import json
import visitor  # references visitor.py in this repo

with open('test.json') as f:
    ast = json.loads(f.read())
    
program = visitor.objectify(ast)  # visitor.Node object
```

At this point, `program` represents a hierarchy of `Node` subclasses:

```
Program
    .body: [VariableDeclaration]
        .declarations: [VariableDeclarator]
            .id: Identifier
                .name: "map"
            .init: ObjectExpression
                .properties: [Property]
                    .key: Literal
                        .value: "abc"
                    .value: Literal
                        .value: 123
```

Suppose we wanted to change `{'abc': 123}` to `{'new-key': 123}`:

```python
object_exp = program.body[0].declarations[0].init  # ObjectExpression
object_exp.properties[0].key.value = "new-key"

# Write out the modified AST
with open('test-modified.json', 'w') as f:
    f.write(json.dumps(program.dict(), indent=2))
```

Finally, the new AST can be turned back into JS code with `esprima` or other tools.

## Testing
The AST traversal has been tested with a dozen of the most complex real-world
JavaScript samples, including popular libraries like JQuery and Sugar and code
served by the Alexa top 10 sites.

To run unit tests, test coverage, linting, and type-checking:

```bash

$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
$ coverage run visitor_test.py  # Unit tests
$ coverage report  # Should show 100%
$ find . -name '*.py' -not -path './venv/*' -exec pylint '{}' +
$ mypy .  # Static type-checking
```
